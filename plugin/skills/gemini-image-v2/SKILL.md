---
name: gemini-image-v2
description: "Genereer afbeeldingen via Google Gemini API (primair) of OpenAI (fallback). Werkt standalone (interactief) en in quick mode (vanuit andere skills). Retourneert een publieke URL."
---

# Gemini Image Generator v2

Genereer afbeeldingen via Google Gemini API (primair) of OpenAI (fallback). Werkt met elke prompt: panda's, productfoto's, illustraties, diagrammen, etc. Detecteert automatisch de omgeving en kiest de juiste methode.

**Referentiebeeld panda:** `https://files.catbox.moe/23dzti.png`
**Providers:** Gemini (met referentie-image, multimodal) → OpenAI (prompt-only) → fallback

---

## Aanroep-interface (voor gebruik vanuit andere skills)

```
Input:  IMAGE_PROMPT (Engelse prompt)
Output: IMAGE_URL (publieke URL of lege string)
```

Als IMAGE_PROMPT al beschikbaar is: sla stap 1 (interactieve vragen) over, ga direct naar stap 2 (API key check).

---

## Stap 1: Input (alleen standalone)

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

**Bij panda-prompts:** Gebruik altijd het fotorealistische karakter:
```
A photorealistic giant panda with a realistic furry head, black eye patches,
and round ears, on a human body wearing a tailored black business suit,
crisp white dress shirt, and a bold orange necktie. The panda has black
furry paws instead of human hands. Confident posture, striding forward as
a leader. Cinematic photography style, natural lighting, sharp focus,
shallow depth of field.
```

**Als gebruiker een eigen beschrijving typt:** Vertaal naar het Engels als dat nog niet zo is, en optimaliseer de prompt licht (voeg compositie/stijl details toe).

Sla op: IMAGE_PROMPT (Engelse prompt), FORMAT_INSTRUCTION (bijv. "square 1:1 aspect ratio")

---

## Stap 2: API key check

Controleer of API keys beschikbaar zijn via de MCP tool `check_api_keys`.

**Response:** `{"gemini": true/false, "openai": true/false}`

**Als minstens één key `true`:** Ga door naar stap 3.

**Als beide `false`:** Vraag de key via AskUserQuestion:
- question: "Geen API keys gevonden. Plak een Gemini of OpenAI API key hieronder. Gemini: https://aistudio.google.com/apikey — OpenAI: https://platform.openai.com/api-keys"
- header: "API Key"
- options:
  - "Ik heb geen key, sla over" — retourneer lege string als IMAGE_URL
  - "Gemini key" — de gebruiker plakt de key via het Other-tekstveld
  - "OpenAI key" — de gebruiker plakt de key via het Other-tekstveld
- multiSelect: false

Als de gebruiker een key plakt:
1. Bepaal de provider op basis van de gekozen optie
2. Sla op via MCP tool `set_api_key` met `provider` ("gemini" of "openai") en `api_key`
3. Exporteer ook in de shell voor curl-fallbacks:
```bash
export GEMINI_API_KEY="[GEPLAKTE_KEY]"   # als Gemini
export OPENAI_API_KEY="[GEPLAKTE_KEY]"   # als OpenAI
```

Als de gebruiker geen key heeft: retourneer lege string als IMAGE_URL. Stop NOOIT de flow.

---

## Stap 3: Omgeving detecteren

```bash
if [ -d "/sessions" ]; then echo "ENVIRONMENT=cowork"; else echo "ENVIRONMENT=local"; fi
```

- **cowork** → Ga naar Stap 4B (MCP server primair, browser fallback)
- **local** → Ga naar Stap 4A (curl)

---

## Stap 4A: Lokaal (curl)

Combineer IMAGE_PROMPT met eventuele FORMAT_INSTRUCTION in de uiteindelijke prompt.

### 4A.1 — Gemini (primair)

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT="/tmp/gemini_${TIMESTAMP}.png"

RESPONSE=$(curl -s -m 120 \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "[IMAGE_PROMPT]. [FORMAT_INSTRUCTION]"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }')

python3 -c "
import json, base64, sys
data = json.loads(sys.stdin.read())
for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
    if 'inlineData' in part:
        with open('$OUTPUT', 'wb') as f:
            f.write(base64.b64decode(part['inlineData']['data']))
        print('OK')
        sys.exit(0)
print('FAIL')
sys.exit(1)
" <<< "$RESPONSE"
```

Als Gemini faalt en OPENAI_API_KEY beschikbaar is, probeer OpenAI:

### 4A.2 — OpenAI (fallback)

```bash
RESPONSE=$(curl -s -m 120 \
  "https://api.openai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-image-1.5",
    "prompt": "[IMAGE_PROMPT]. [FORMAT_INSTRUCTION]",
    "n": 1,
    "size": "1024x1024",
    "quality": "high"
  }')

python3 -c "
import json, base64, sys
data = json.loads(sys.stdin.read())
for item in data.get('data', []):
    if 'b64_json' in item:
        with open('$OUTPUT', 'wb') as f:
            f.write(base64.b64decode(item['b64_json']))
        print('OK')
        sys.exit(0)
print('FAIL')
sys.exit(1)
" <<< "$RESPONSE"
```

### 4A.3 — Upload

```bash
# Upload: catbox.moe (primair), tmpfiles.org (fallback)
IMAGE_URL=$(curl -s -F "reqtype=fileupload" -F "fileToUpload=@$OUTPUT" https://catbox.moe/user/api.php)
if [ -z "$IMAGE_URL" ] || ! echo "$IMAGE_URL" | grep -q "^http"; then
    TMPFILES_RESP=$(curl -s -F "file=@$OUTPUT" https://tmpfiles.org/api/v1/upload)
    IMAGE_URL=$(echo "$TMPFILES_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['url'].replace('tmpfiles.org/','tmpfiles.org/dl/',1).replace('http://','https://'))" 2>/dev/null)
fi
echo "URL: $IMAGE_URL"
```

**Error handling:**
- Gemini API fout → OpenAI fallback → lege string
- Upload faalt → probeer andere host, daarna placeholder

**Output:** Toon de publieke URL en een korte bevestiging.

---

## Stap 4B: Cowork (MCP server primair, browser fallback)

### 4B.0 — MCP server (primair)

Gebruik de MCP tool `generate_custom_image` met de IMAGE_PROMPT + FORMAT_INSTRUCTION:

```
MCP tool: generate_custom_image
  prompt: "[IMAGE_PROMPT]. [FORMAT_INSTRUCTION]"
```

Parse de JSON-response:
- `success: true` → `image_url` is IMAGE_URL. Klaar. (response bevat ook `provider`)
- `success: false` + `fallback_url` aanwezig → gebruik `fallback_url` als IMAGE_URL. Klaar.
- `success: false` zonder `fallback_url` → ga naar stap 4B.1 (browser fallback).

### 4B.1 — Tab verkrijgen (browser fallback)

MCP tool: `tabs_context_mcp` met `createIfEmpty: true`
Sla het `tabId` op.

### 4B.2 — Navigeer naar JS-context

MCP tool: `navigate` naar `https://example.com` met het tabId.

### 4B.3 — Genereer image via Gemini API

MCP tool: `javascript_tool` in het tabId:

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
Als er een fout is: ga naar fallback-keten.

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

### 4B.6 — Upload voor publieke URL

Alleen nodig als een publieke URL gewenst is (bijv. vanuit klantpagina flow).

**Methode A: upload_image_base64 MCP tool (primair, geen CORS)**

Haal de base64 data op uit de browser:
```javascript
(() => window._geminiB64 || 'NO_DATA')()
```

Geef door aan:
```
MCP tool: upload_image_base64
  image_base64: "[BASE64_DATA]"
  filename: "gemini-image.png"
```

Parse de JSON-response: `success: true` → `image_url` is IMAGE_URL.

**Methode B: Browser-side upload (fallback als MCP tool faalt)**

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
    return JSON.stringify({ error: e.message, note: 'CORS blocked? Use placeholder.' });
  }
})()
```

**Standalone output:** Toon de screenshot en meld dat het bestand gedownload is.

---

## Fallback-keten

```
Lokaal:
  Gemini + referentie (MCP) → OpenAI prompt-only (MCP) → Gemini curl → OpenAI curl → lege string

Cowork:
  1. MCP generate_custom_image (Gemini+ref → OpenAI intern)
  2. success:false + fallback_url → gebruik fallback_url
  3. Browser JS Gemini+ref → upload_image_base64
  4. Browser JS fetch + catbox browser upload
  5. Lege string (flow stopt nooit)
```

---

## Foutafhandeling

Bij elke fout: ga door naar het volgende niveau in de fallback-keten. Retourneer uiteindelijk altijd een IMAGE_URL (publieke URL of lege string). Stop NOOIT de flow.
