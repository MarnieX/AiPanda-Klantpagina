---
name: gemini-image
description: "Genereer afbeeldingen via Google Gemini API. Geef een beschrijving of laat een prompt bouwen op basis van context. Retourneert een publieke URL. Werkt in Cowork en lokaal."
---

# Gemini Image Generator

Genereer afbeeldingen via Google Gemini API. Werkt met elke prompt: panda's, productfoto's, illustraties, diagrammen, etc. Gebruikt curl (geen Python httpx), dus werkt ook in Cowork.

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

## Stap 3: Genereer en upload

Combineer IMAGE_PROMPT met eventuele FORMAT_INSTRUCTION in de uiteindelijke prompt.

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT="/tmp/gemini_${TIMESTAMP}.png"

# Gemini API via curl (werkt in Cowork, geen httpx nodig)
RESPONSE=$(curl -s -m 120 \
  "https://generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent?key=$GEMINI_API_KEY" \
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
# Toon response voor debugging
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

## Gebruik vanuit andere skills

Deze skill kan aangeroepen worden als referentie vanuit andere skills. Het curl-patroon (stap 3) is het kernmechanisme dat hergebruikt kan worden:

1. Bouw een prompt
2. Curl naar Gemini API met `responseModalities: ["TEXT", "IMAGE"]`
3. Decodeer base64 response naar PNG
4. Upload naar catbox.moe

Andere skills hoeven niet de volledige flow te doorlopen (AskUserQuestion etc.), maar kunnen direct het curl-patroon gebruiken met een zelfgebouwde prompt.
