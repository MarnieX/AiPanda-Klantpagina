---
name: gemini-image
description: "Genereer afbeeldingen via Google Gemini API. Geef een beschrijving of laat een prompt bouwen op basis van context. Retourneert een publieke URL. Werkt in Cowork (via browser MCP) en lokaal (via curl)."
---

# Gemini Image Generator

Genereer afbeeldingen via Google Gemini API. Werkt met elke prompt: panda's, productfoto's, illustraties, diagrammen, etc. Detecteert automatisch de omgeving en kiest de juiste methode.

**Referentiebeeld panda:** `https://files.catbox.moe/23dzti.png`

---

## Stap 1: Input

Twee modi: direct (gebruiker beschrijft zelf) of guided (Claude bouwt prompt).

Gebruik AskUserQuestion:
- question: "Wat voor afbeelding wil je genereren? Beschrijf het zo specifiek mogelijk, of kies 'Bouw een prompt voor mij'."
- header: "Afbeelding"
- options:
  - "Bouw een prompt voor mij" — Claude stelt vervolgvragen en bouwt een geoptimaliseerde Engelse prompt
  - "Ik typ mijn eigen beschrijving" — de gebruiker typt via Other een directe beschrijving
- multiSelect: false

**Als "Bouw een prompt voor mij":** Stel vervolgvragen via AskUserQuestion:

1. Onderwerp:
   - question: "Wat moet er op de afbeelding staan? Beschrijf het onderwerp."
   - header: "Onderwerp"
   - options: "Een panda mascotte", "Een productfoto", "Een abstracte illustratie" — gebruiker typt via Other
   - multiSelect: false

2. Stijl:
   - question: "Welke stijl wil je?"
   - header: "Stijl"
   - options:
     - "Fotorealistisch (Recommended)" — levensechte beelden
     - "Cartoon/illustratie" — speels en grafisch
     - "Artistiek/abstract" — creatief en expressief
     - "Zakelijk/clean" — professioneel en minimalistisch
   - multiSelect: false

3. Formaat:
   - question: "Welk formaat?"
   - header: "Formaat"
   - options:
     - "1:1 vierkant (Recommended)" — social media, profielfoto's
     - "16:9 landscape" — presentaties, headers
     - "9:16 portrait" — stories, posters
   - multiSelect: false

Bouw op basis van de antwoorden een geoptimaliseerde Engelse prompt. Voeg stijl- en compositie-instructies toe.

**Als gebruiker een eigen beschrijving typt:** Vertaal naar het Engels als dat nog niet zo is, en optimaliseer de prompt licht (voeg compositie/stijl details toe).

Sla op: IMAGE_PROMPT (Engelse prompt), FORMAT_INSTRUCTION (bijv. "square 1:1 aspect ratio")

---

## Stap 2: GEMINI_API_KEY check

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+OK}"
```

Als dit NIET "OK" print:

Vraag de key via AskUserQuestion:
- question: "GEMINI_API_KEY ontbreekt. Plak je Gemini API key hieronder (aanmaken op https://aistudio.google.com/apikey)."
- header: "API Key"
- options:
  - "Ik heb geen key, annuleer" — stop de skill
  - "Key komt eraan" — de gebruiker plakt de key via het Other-tekstveld
- multiSelect: false

Als de gebruiker een key plakt:
```bash
export GEMINI_API_KEY="[GEPLAKTE_KEY]"
echo "[DIAG] Key geactiveerd voor deze sessie"
```

Als de gebruiker geen key heeft: meld dit en stop. Zonder key kan er geen afbeelding gegenereerd worden.

---

## Stap 3: Omgeving detecteren

```bash
if [ -d "/sessions" ]; then echo "ENVIRONMENT=cowork"; else echo "ENVIRONMENT=local"; fi
```

- **cowork** → Ga naar Stap 4B (browser MCP)
- **local** → Ga naar Stap 4A (curl)

---

## Stap 4A: Lokaal (curl)

Combineer IMAGE_PROMPT met eventuele FORMAT_INSTRUCTION in de uiteindelijke prompt.

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT="/tmp/gemini_${TIMESTAMP}.png"

# Gemini API via curl
RESPONSE=$(curl -s -m 120 \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "[IMAGE_PROMPT]. [FORMAT_INSTRUCTION]"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }')

# Decodeer base64 naar PNG
python3 -c "
import json, base64, sys
data = json.loads(sys.stdin.read())
for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
    if 'inlineData' in part:
        with open('$OUTPUT', 'wb') as f:
            f.write(base64.b64decode(part['inlineData']['data']))
        print('OK: afbeelding opgeslagen als $OUTPUT')
        sys.exit(0)
print('FAIL: geen afbeelding in response')
print(json.dumps(data, indent=2)[:500], file=sys.stderr)
sys.exit(1)
" <<< "$RESPONSE"

# Upload naar catbox.moe voor publieke URL
IMAGE_URL=$(curl -s -F "reqtype=fileupload" -F "fileToUpload=@$OUTPUT" https://catbox.moe/user/api.php)
echo "URL: $IMAGE_URL"
```

**Error handling:**
- Als de Gemini API een fout retourneert: toon de foutmelding en meld dat de generatie mislukt is.
- Als catbox upload faalt: probeer nogmaals, of meld de lokale padnaam als fallback.

**Output:** Toon de publieke URL en een korte bevestiging:
```
Afbeelding gegenereerd en geupload:
URL: [IMAGE_URL]
Lokaal bestand: [OUTPUT]
```

---

## Stap 4B: Cowork (browser MCP)

In Cowork blokkeert de sandbox-proxy uitgaand HTTP-verkeer. De enige route naar buiten is via de Chrome MCP-bridge: Claude bestuurt de lokale Chrome van de gebruiker.

### 4B.1 — Tab verkrijgen

MCP tool: `tabs_context_mcp` met `createIfEmpty: true`
Sla het `tabId` op.

### 4B.2 — Navigeer naar JS-context

MCP tool: `navigate` naar `https://example.com` met het tabId.
Dit geeft een schone pagina om JavaScript uit te voeren.

### 4B.3 — Genereer image via Gemini API

MCP tool: `javascript_tool` in het tabId. Voer dit script uit:

```javascript
(async () => {
  try {
    const API_KEY = '[GEMINI_API_KEY]';
    const MODEL = 'gemini-3-pro-image-preview';
    const PROMPT = '[IMAGE_PROMPT]. [FORMAT_INSTRUCTION]';
    const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;

    const resp = await fetch(URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: PROMPT }] }],
        generationConfig: { responseModalities: ['TEXT', 'IMAGE'] }
      })
    });

    const data = await resp.json();
    if (!resp.ok) return JSON.stringify({ error: data.error?.message });

    const parts = data.candidates?.[0]?.content?.parts || [];
    for (const part of parts) {
      if (part.inlineData) {
        window._geminiB64 = part.inlineData.data;
        window._geminiMime = part.inlineData.mimeType;
      }
    }

    return JSON.stringify({
      success: true,
      hasImage: !!window._geminiB64,
      imageSize: window._geminiB64?.length || 0
    });
  } catch(e) {
    return JSON.stringify({ error: e.message });
  }
})()
```

Als `success: true` en `hasImage: true`: ga door naar 4B.4.
Als er een fout is: meld de fout en ga naar de fallback (placeholder URL).

### 4B.4 — Download naar lokale machine

MCP tool: `javascript_tool` in het tabId:

```javascript
(() => {
  const a = document.createElement('a');
  a.href = 'data:' + window._geminiMime + ';base64,' + window._geminiB64;
  a.download = 'gemini-image.png';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  return 'Download triggered';
})()
```

### 4B.5 — Render + screenshot als bewijs

MCP tool: `javascript_tool` in het tabId:

```javascript
(() => {
  const img = document.createElement('img');
  img.src = 'data:' + window._geminiMime + ';base64,' + window._geminiB64;
  img.style.cssText = 'max-width:90%;max-height:80vh';
  document.body.innerHTML = '';
  document.body.appendChild(img);
  return 'Image rendered';
})()
```

Daarna: MCP tool `computer` (screenshot) om de afbeelding als bewijs in het gesprek te tonen.

### 4B.6 — (Optioneel) Upload naar catbox.moe voor publieke URL

Alleen nodig als een publieke URL gewenst is (bijv. vanuit klantpagina flow).

MCP tool: `javascript_tool` in het tabId:

```javascript
(async () => {
  try {
    const b64 = window._geminiB64;
    const mime = window._geminiMime || 'image/png';
    const byteChars = atob(b64);
    const byteArray = new Uint8Array(byteChars.length);
    for (let i = 0; i < byteChars.length; i++) byteArray[i] = byteChars.charCodeAt(i);
    const blob = new Blob([byteArray], { type: mime });

    const form = new FormData();
    form.append('reqtype', 'fileupload');
    form.append('fileToUpload', blob, 'panda.png');
    const resp = await fetch('https://catbox.moe/user/api.php', {
      method: 'POST',
      body: form
    });
    const url = await resp.text();
    return JSON.stringify({ success: true, url: url.trim() });
  } catch(e) {
    return JSON.stringify({ error: e.message, note: 'CORS blocked? Try same-origin.' });
  }
})()
```

**Als CORS blokkeert:** Navigeer naar `https://catbox.moe` (same-origin) en voer de upload daar uit:

1. MCP tool: `navigate` naar `https://catbox.moe`
2. MCP tool: `javascript_tool`:
```javascript
(async () => {
  try {
    const b64 = window._geminiB64;
    // b64 data overleeft navigatie niet, dus moet opnieuw worden doorgegeven
    // Als window._geminiB64 undefined is, geef een foutmelding terug
    if (!b64) return JSON.stringify({ error: 'Image data lost after navigation. Use placeholder.' });

    const mime = window._geminiMime || 'image/png';
    const byteChars = atob(b64);
    const byteArray = new Uint8Array(byteChars.length);
    for (let i = 0; i < byteChars.length; i++) byteArray[i] = byteChars.charCodeAt(i);
    const blob = new Blob([byteArray], { type: mime });

    const form = new FormData();
    form.append('reqtype', 'fileupload');
    form.append('fileToUpload', blob, 'panda.png');
    const resp = await fetch('/user/api.php', {
      method: 'POST',
      body: form
    });
    const url = await resp.text();
    return JSON.stringify({ success: true, url: url.trim() });
  } catch(e) {
    return JSON.stringify({ error: e.message });
  }
})()
```

**Let op:** Na navigatie gaat `window._geminiB64` verloren. Om dit op te lossen, sla de base64 data op in een JS-variabele VOORDAT je navigeert, of voer generatie + upload op dezelfde pagina uit. Als de data verloren is, gebruik de placeholder URL.

**Output voor standalone gebruik:** Toon de screenshot en meld dat het bestand gedownload is naar de lokale Downloads-map.

---

## Fallback-keten

```
Lokaal:
  Curl naar Gemini API → Catbox upload → Publieke URL
  Fallback: Placeholder URL

Cowork:
  Browser JS fetch (Gemini API) → Download + Screenshot
  Voor publieke URL: + Catbox upload vanuit browser JS → URL
  Als catbox CORS faalt: navigeer naar catbox.moe → same-origin upload
  Laatste fallback: Placeholder URL (flow stopt nooit)
```

---

## Gebruik vanuit andere skills

Deze skill kan aangeroepen worden als referentie vanuit andere skills. Het patroon verschilt per omgeving:

**Lokaal:** Het curl-patroon (stap 4A) is het kernmechanisme.
**Cowork:** De browser MCP flow (stap 4B) met 5 MCP-calls.

Andere skills hoeven niet de volledige flow te doorlopen (AskUserQuestion etc.), maar kunnen direct het juiste patroon gebruiken met een zelfgebouwde prompt.
