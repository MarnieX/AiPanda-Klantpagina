---
name: klantpagina
description: "Genereer een professionele Notion-klantpagina voor AI Panda met persoonlijke toekomstvisie. Haalt bedrijfsinfo en merkidentiteit op, leest consultants uit een Excel, genereert een AI Panda-afbeelding, schrijft een visionair toekomstverhaal en maakt een complete Notion-pagina met roadmap en wow-factor."
---

# AI Panda Klantpagina Generator

Je genereert een professionele Notion-klantpagina voor AI Panda. Volg de stappen exact in volgorde. Start parallelstappen altijd tegelijk om snelheid te winnen.

Gebruik TodoWrite om voortgang te tonen:
1. Bedrijfsnaam ophalen
2. Bedrijfsinfo + merkidentiteit + Excel laden (parallel), daarna sectorprobleem
3. Consultants selecteren
4. Bevestiging vragen (incl. merkidentiteit + sectorprobleem)
5. Panda-afbeelding + roadmap + quiz-URL + toekomstverhaal (parallel), daarna visie-afbeelding
6. Notion-pagina aanmaken (quiz is geintegreerd als link)

---

## Stap 1: Vraag om bedrijf

Vraag de gebruiker: "Voor welk bedrijf wil je een klantpagina maken? Geef de bedrijfsnaam of website-URL."

Gebruik hiervoor GEEN AskUserQuestion (dat vereist opties). Stel de vraag als gewone tekst en wacht op het antwoord.

Sla op: KLANT_INPUT (naam of URL zoals ingetypt door gebruiker)

---

## Stap 2: Parallel ophalen (2A + 2B tegelijk, daarna 2A2)

### 2A — Bedrijfsinfo ophalen

Gebruik WebSearch met twee queries (parallel als mogelijk):
1. `"[klant] Nederland bedrijf sector omschrijving"` — voor BEDRIJFSNAAM, OMSCHRIJVING, SECTOR
2. `"[klant] huisstijl merkidentiteit kleuren tagline"` — voor MERKIDENTITEIT

Als KLANT_INPUT een URL of domein bevat, gebruik dat als WEBSITE_DOMEIN. Anders, leid het domein af uit de WebSearch-resultaten.

Fallback: als WebSearch geen bruikbare resultaten oplevert, gebruik de naam zoals ingetypt, omschrijving leeg laten voor bevestigingsstap. Gebruik voor MERKIDENTITEIT generieke waarden (donkerblauw #1a365d, zakelijke stijl) en meld dit in het bevestigingsscherm.

**Diagnostics:** Meld altijd welke methode gebruikt is:
- `[DIAG 2A] WebSearch geslaagd`
- `[DIAG 2A] WebSearch gefaald → handmatige invoer`

Sla op: BEDRIJFSNAAM, OMSCHRIJVING, SECTOR, WEBSITE_DOMEIN (bijv. `bol.com`, zonder https://), MERKIDENTITEIT (kleuren met hex-codes, tagline, visuele stijl, kenmerkende elementen)

### 2A2 — Sectorprobleem identificeren

**Wacht op 2A** (SECTOR moet beschikbaar zijn). Voer uit zodra 2A klaar is, via WebSearch:
- Query: "[SECTOR] grootste structurele probleem AI oplossing komende 10 jaar"
- Zoek naar fundamentele knelpunten die de hele sector raken (capaciteitstekorten, informatiefragmentatie, veiligheidsvraagstukken, regulatoire complexiteit, etc.)
- Denk niet aan kleine efficiëntiewinsten maar aan structurele verschuivingen

**Diagnostics:** `[DIAG 2A2] Sectorprobleem gevonden: [korte omschrijving]`

Sla op: SECTORPROBLEEM (het kernprobleem dat AI in 10 jaar fundamenteel kan oplossen voor deze sector)

### 2B — Excel lezen (alle teamleden laden)

Zoek het Excel-bestand via het plugin-pad (betrouwbaarst in Cowork) met find als fallback:

```bash
pip install openpyxl --break-system-packages -q 2>/dev/null

# Primair: plugin-pad (werkt betrouwbaar in Cowork)
EXCEL_PATH=""
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/data/ai-panda-team.xlsx" ]; then
    EXCEL_PATH="$CLAUDE_PLUGIN_ROOT/data/ai-panda-team.xlsx"
    echo "[DIAG 2B] Gevonden via CLAUDE_PLUGIN_ROOT: $EXCEL_PATH"
fi

# Fallback: find (voor lokale ontwikkeling of als plugin-pad niet werkt)
if [ -z "$EXCEL_PATH" ]; then
    echo "[DIAG 2B] CLAUDE_PLUGIN_ROOT niet beschikbaar, zoeken via find..."
    EXCEL_PATH=$(find /sessions ~ -maxdepth 10 -name "ai-panda-team.xlsx" 2>/dev/null | head -1)
fi

if [ -z "$EXCEL_PATH" ]; then
    echo "[DIAG 2B] NIET GEVONDEN. Mapstructuur van /sessions voor debug:"
    find /sessions -maxdepth 5 -type d 2>/dev/null | head -30
    echo "[DIAG 2B] Home directory inhoud:"
    ls ~ 2>/dev/null | head -20
    echo '{"error": "ai-panda-team.xlsx niet gevonden"}'
else
    echo "[DIAG 2B] Gevonden op: $EXCEL_PATH"
    EXCEL_PATH="$EXCEL_PATH" python3 << 'PYEOF'
import openpyxl, json, os, sys

path = os.environ["EXCEL_PATH"]
wb = openpyxl.load_workbook(path)
ws = wb.active

# Dynamische header-detectie (voorkomt crashes bij kolom-wijzigingen)
headers = [str(cell or "").strip().lower() for cell in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
team = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0]:
        entry = {}
        for i, h in enumerate(headers):
            entry[h] = str(row[i] or "") if i < len(row) else ""
        team.append({
            "naam": entry.get("naam", ""),
            "functie": entry.get("functie", ""),
            "foto_url": entry.get("foto-url", entry.get("foto_url", "")),
            "email": entry.get("e-mail", entry.get("email", ""))
        })
print(f"[DIAG 2B] {len(team)} teamleden geladen", file=sys.stderr)
print(f"[DIAG 2B] Headers gevonden: {headers}", file=sys.stderr)
print(json.dumps(team, indent=2, ensure_ascii=False))
PYEOF
fi
```

Sla op: ALLE_TEAMLEDEN (volledige lijst met naam, functie, foto_url, email per teamlid)

Fallback als Excel niet gevonden: ga door zonder teamdata, vraag namen handmatig in stap 3. GA ALTIJD DOOR.

---

## Stap 3: Vraag om consultants (multiSelect)

Gebruik AskUserQuestion met dynamische opties uit de Excel:
- question: "Welke consultants werken aan dit traject?"
- header: "Team"
- multiSelect: true
- options: dynamisch opgebouwd uit ALLE_TEAMLEDEN, bijv:
  - label: "Marnix", description: "Project Lead"
  - label: "Noud", description: "Developer"
  - label: "Rick", description: "Ai Consultant"
  - label: "Jack", description: "Co-Founder / Consultant"

**BELANGRIJK:** AskUserQuestion ondersteunt max 4 opties. Als er meer dan 4 teamleden zijn:
- Toon de eerste 4 als opties
- De gebruiker kan via "Other" extra namen toevoegen

**Fallback als Excel niet gevonden:** Stel een open tekstvraag: "Welke consultants werken aan dit traject? Typ de namen gescheiden door komma's."

Sla op: CONSULTANTS (lijst met naam, functie, foto_url, email per geselecteerde consultant, gematcht aan ALLE_TEAMLEDEN)

---

## Stap 4: Bevestigingsscherm

Toon de opgehaalde informatie overzichtelijk aan de gebruiker:

```
Samenvatting:

Bedrijf: [BEDRIJFSNAAM]
Website: [WEBSITE_DOMEIN]
Sector: [SECTOR]

Over het bedrijf:
[OMSCHRIJVING]

Merkidentiteit: [MERKIDENTITEIT — kleuren, tagline, visuele stijl]
Sectorprobleem voor toekomstvisie: [SECTORPROBLEEM — kort]

Consultants:
- [NAAM_1] — [FUNCTIE_1]
- [NAAM_2] — [FUNCTIE_2]
- [NAAM_3] — [FUNCTIE_3]
```

Gebruik daarna AskUserQuestion:
- question: "Klopt bovenstaande informatie, of wil je iets aanpassen?"
- header: "Bevestiging"
- options:
  - "Ziet er goed uit, ga door" (Recommended)
  - "Bedrijfsinfo aanpassen"
  - "Consultants aanpassen"

Als de gebruiker wil aanpassen: vraag wat er anders moet en verwerk de correctie. Herhaal het bevestigingsscherm daarna niet opnieuw — vertrouw op de aanpassing en ga door.

---

## Stap 5: Parallel uitvoeren (5A + 5B + 5C + 5D tegelijk, daarna 5E na 5D)

### 5A — AI Panda-afbeelding genereren

**Referentiebeeld:** `https://files.catbox.moe/23dzti.png`

**Pre-check: controleer of GEMINI_API_KEY beschikbaar is.**
```bash
echo "[DIAG 5A] GEMINI_API_KEY check: ${GEMINI_API_KEY:+OK}"
```

Als dit NIET "OK" print:
1. Vraag de gebruiker om de key via AskUserQuestion:
   - question: "GEMINI_API_KEY ontbreekt. Plak je Gemini API key hieronder (aanmaken op https://aistudio.google.com/apikey)."
   - header: "API Key"
   - options: twee opties: "Ik heb geen key, sla over" en "Key komt eraan" (de gebruiker plakt de key via het Other-tekstveld)
2. Als de gebruiker een key plakt, sla deze op en maak beschikbaar:
```bash
export GEMINI_API_KEY="[GEPLAKTE_KEY]"
echo "[DIAG 5A] Key geactiveerd voor deze sessie"
```
3. Als de gebruiker geen key heeft, ga door met de fallback-afbeelding. Stop NOOIT de flow.

**Panda-prompt:** Claude bouwt zelf een beschrijvende Engelse prompt op basis van BEDRIJFSNAAM, SECTOR en WEBSITE_DOMEIN. Voorbeeld:
```
A friendly cartoon red panda mascot in a navy blue business polo shirt
with "[BEDRIJFSNAAM]" embroidered on the chest, standing confidently
in a modern office presenting AI solutions on a whiteboard.
Professional illustration, clean white background.
```

**Omgeving detecteren:**
```bash
if [ -d "/sessions" ]; then echo "ENVIRONMENT=cowork"; else echo "ENVIRONMENT=local"; fi
```

---

#### Lokaal (ENVIRONMENT=local)

**Methode 1: Python script (volledige pipeline met logo/referentie):**
```bash
echo "[DIAG 5A] Zoeken naar generate_notion_image.py..."
SCRIPT=$(find /sessions ~ -maxdepth 10 -name "generate_notion_image.py" 2>/dev/null | head -1)

if [ -z "$SCRIPT" ]; then
    echo "[DIAG 5A] Script niet gevonden, ga naar curl-fallback"
else
    echo "[DIAG 5A] Script gevonden op: $SCRIPT"
    SAFE_NAME=$(echo "[BEDRIJFSNAAM]" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
    cd "$(dirname "$SCRIPT")" && python3 generate_notion_image.py \
      --client \
      --company-name "[BEDRIJFSNAAM]" \
      --sector "[SECTOR]" \
      --logo-domain "[WEBSITE_DOMEIN]" \
      --output "/tmp/panda_${SAFE_NAME}.png" \
      --upload --json
fi
```

De `url` uit de JSON-output is PANDA_IMAGE_URL.

**Methode 2 (fallback): curl-aanpak:**

Als methode 1 faalt (connectiefout, httpx error, script niet gevonden):

```bash
SAFE_NAME=$(echo "[BEDRIJFSNAAM]" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
OUTPUT="/tmp/panda_${SAFE_NAME}.png"

RESPONSE=$(curl -s -m 120 \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "[PANDA_PROMPT]"}]}],
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
        print('OK')
        sys.exit(0)
print('FAIL')
sys.exit(1)
" <<< "$RESPONSE"

# Upload naar catbox.moe
PANDA_IMAGE_URL=$(curl -s -F "reqtype=fileupload" -F "fileToUpload=@$OUTPUT" https://catbox.moe/user/api.php)
echo "[DIAG 5A] Curl-fallback URL: $PANDA_IMAGE_URL"
```

---

#### Cowork (ENVIRONMENT=cowork)

In Cowork blokkeert de sandbox-proxy uitgaand HTTP-verkeer voor directe Python/curl calls. Er zijn twee routes: de MCP server (primair, werkt nu dankzij socksio fix) en de Chrome MCP-bridge (fallback).

**Methode 1: MCP server tools (primair)**

Gebruik de MCP tool `generate_custom_image` of `generate_panda_image` (afhankelijk van context). Deze tools genereren de afbeelding via Gemini EN uploaden naar catbox.moe server-side (geen CORS-problemen).

```
MCP tool: generate_panda_image
  bedrijfsnaam: "[BEDRIJFSNAAM]"
```

Parse de JSON-response:
- `success: true` → `image_url` is PANDA_IMAGE_URL
- `success: false` → ga naar Methode 2

**Methode 2: Browser JS + upload_image_base64 MCP tool (fallback)**

Als Methode 1 faalt, gebruik de Chrome MCP-bridge om de afbeelding te genereren in de browser, en upload via de MCP server tool `upload_image_base64` (server-side curl, geen CORS).

**5A-C.1 — Tab verkrijgen:**
MCP tool: `tabs_context_mcp` met `createIfEmpty: true`. Sla `tabId` op.

**5A-C.2 — Navigeer naar JS-context:**
MCP tool: `navigate` naar `https://example.com` met het tabId.

**5A-C.3 — Genereer image via Gemini API:**
MCP tool: `javascript_tool` in het tabId:

```javascript
(async () => {
  try {
    const API_KEY = '[GEMINI_API_KEY]';
    const MODEL = 'gemini-3-pro-image-preview';
    const PROMPT = '[PANDA_PROMPT]';
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

**5A-C.4 — Upload via MCP server tool (geen CORS):**

Haal de base64 data op uit de browser en geef deze door aan de MCP server tool `upload_image_base64`. Dit omzeilt CORS omdat de upload server-side via curl gebeurt.

MCP tool: `javascript_tool` in het tabId om de base64 data op te halen:
```javascript
(() => window._geminiB64 ? window._geminiB64.substring(0, 50000) : 'NO_DATA')()
```

**Let op:** Als de base64 string te groot is voor een enkele MCP call, splits dan in chunks of gebruik `generate_custom_image` (Methode 1) in plaats daarvan.

Geef de volledige base64 string door aan:
```
MCP tool: upload_image_base64
  image_base64: "[BASE64_DATA]"
  filename: "panda_[bedrijfsnaam].png"
```

Parse de JSON-response: `success: true` → `image_url` is PANDA_IMAGE_URL.

**5A-C.5 — Screenshot als bewijs:**
MCP tool: `javascript_tool` om de afbeelding te renderen:
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
Daarna: MCP tool `computer` (screenshot) als bewijs.

---

#### Fallback-keten (beide omgevingen)

```
Lokaal:
  Python script → Curl fallback → Placeholder URL

Cowork:
  1. MCP generate_custom_image / generate_panda_image (primair, server-side)
  2. Browser JS fetch + upload_image_base64 MCP tool (fallback, omzeilt CORS)
  3. Browser JS fetch + catbox browser upload (laatste poging)
  4. Placeholder URL
```

**Diagnostics:** Meld altijd welke methode gebruikt is:
- `[DIAG 5A] Lokaal: Python script geslaagd`
- `[DIAG 5A] Lokaal: curl-fallback gebruikt`
- `[DIAG 5A] Cowork: MCP generate_panda_image geslaagd`
- `[DIAG 5A] Cowork: browser + upload_image_base64 fallback gebruikt`
- `[DIAG 5A] Cowork: browser + catbox browser upload gebruikt`
- `[DIAG 5A] Placeholder URL (laatste fallback)`

**Laatste fallback:** gebruik `https://ui-avatars.com/api/?name=AI+Panda&size=400&background=000000&color=ffffff&bold=true&format=png` en meld dit kort. GA ALTIJD DOOR.

### 5B — Roadmap content voorbereiden

Bereid de sector-specifieke roadmap voor (geen externe call nodig, kan meteen):

Maak elke fase specifiek voor SECTOR en BEDRIJFSNAAM. Vermijd generieke tekst. Voorbeelden per sector:
- Retail/e-commerce → productaanbevelingen, voorraadbeheer, vraagvoorspelling
- Zorg → patiëntmonitoring, planningsoptimalisatie, medische beeldherkenning
- Logistiek → routeoptimalisatie, voorspellend onderhoud, warehouse-automatisering
- Fintech → fraudedetectie, risicobeoordeling, chatbot-automatisering
- B2B/dienstverlening → offerteautomatisering, kennismanagement, CRM-verrijking

Sla op als ROADMAP_CONTENT (markdown tekst voor fase 1 t/m 4).

### 5C — Interactieve quiz genereren (JSON + URL)

Input: BEDRIJFSNAAM, SECTOR (beschikbaar na stap 2A)

Genereer 5 sector-specifieke meerkeuzevragen. Volg exact dezelfde instructies als in `.claude/skills/ai-quiz/SKILL.md` stap 1.

**Structuur per vraag:**
- Vraagstelling (helder en direct)
- 3 Antwoordopties (A/B/C) oplopend in volwassenheid (A=Start, B=Groei, C=Leider)
- Scoring: A = 1 punt, B = 2 punten, C = 3 punten

**Inhoudelijke focus:**
1. **Algemeen:** Hoe wordt AI nu gebruikt in dagelijkse processen?
2. **Data:** Hoe is data in de [SECTOR] georganiseerd? (Noem specifieke data zoals patiëntdossiers, kassabonnen of logistieke logs).
3. **Proces:** Welke [SECTOR]-processen zijn geautomatiseerd? (Noem specifieke processen zoals roostering, orderpicking of triage).
4. **Team:** Hoe staat het team tegenover werken met AI-tools?
5. **Strategie:** Wat is de strategische visie op AI?

**Tone-of-voice:**
- Schrijf de vragen en antwoorden direct aan de klant
- Zorg dat de toon uitnodigend is en niet als een examen aanvoelt
- Antwoord A is niet 'fout', maar een startpunt met potentie
- Gebruik vakterminologie die past bij de sector

**Structureer als JSON** (exact dit format):

```json
{
  "bedrijf": "[BEDRIJFSNAAM]",
  "sector": "[SECTOR]",
  "vragen": [
    {
      "vraag": "Hoe wordt AI nu gebruikt in jullie dagelijkse processen?",
      "opties": [
        {"label": "A", "tekst": "We gebruiken nog geen AI-tools", "score": 1},
        {"label": "B", "tekst": "Enkele medewerkers experimenteren", "score": 2},
        {"label": "C", "tekst": "AI is structureel ingebed", "score": 3}
      ]
    }
  ]
}
```

**Base64-encode en bouw de quiz-URL:**

```bash
QUIZ_BASE_URL="https://marniex.github.io/aipanda-quiz"
QUIZ_JSON='[DE GEGENEREERDE JSON]'

# Base64-encode (URL-safe)
B64=$(echo -n "$QUIZ_JSON" | base64 | tr -d '\n')

# Bouw de volledige URL
QUIZ_URL="${QUIZ_BASE_URL}/#data=${B64}"

echo "$QUIZ_URL"

# Verificatie: decodeer terug om te controleren dat JSON intact is
echo "$B64" | base64 -d | python3 -m json.tool
```

**Fallback als base64-encoding faalt:** Gebruik Python:
```bash
python3 -c "import base64, json; print(base64.b64encode(json.dumps([DATA]).encode()).decode())"
```

Sla op als QUIZ_URL.

### 5D — Toekomstverhaal schrijven

Input: BEDRIJFSNAAM, SECTOR, OMSCHRIJVING, SECTORPROBLEEM (beschikbaar na stap 2)

Schrijf een visionair verhaal van **350-500 woorden** in het Nederlands over hoe [BEDRIJFSNAAM] er over 10 jaar uitziet dankzij AI.

**Structuur** (schrijf als doorlopend proza, geen kopjes of bullets):

1. **Opening met een persoon** — Begin met een concreet, levendig beeld van een medewerker op een gewone werkdag in 2035. Wie is dit? Wat doet ze? Wat ziet ze? Maak het zo specifiek dat het voelt als een scene, niet als een beschrijving.

2. **Het sectorprobleem dat opgelost is** — Laat zien hoe het SECTORPROBLEEM er destijds uitzag en hoe AI dat nu fundamenteel heeft opgelost. Dit is het visionaire hart: niet "processen zijn efficienter", maar een echte structurele verschuiving die 10 jaar geleden ondenkbaar was.

3. **Bedrijfsbrede transformatie** — Zoom uit naar het bedrijf als geheel. Hoe staat het er voor in de markt? Wat kunnen ze nu wat niemand anders kan? Hoe ziet de klantrelatie eruit?

4. **Terug naar de mens** — Eindig bij de persoon uit de opening. Hoe ervaart zij haar werk? Wat heeft de transformatie voor haar betekend? Kort, concreet, menselijk.

**Toon**: Warm, zelfverzekerd, visionair. Niet wollig of generiek. Niet vol jargon. Geen sciencefiction. Ambitieus maar aards.

**Visionair betekent**: dingen beschrijven die vandaag nog niet bestaan of niet op deze schaal werken. Autonome systemen, AI die sectorbrede coordinatieproblemen oplost, nieuwe samenwerkingsvormen, diensten die vijf jaar geleden conceptueel ondenkbaar waren.

**Wat je vermijdt**:
- Generieke uitspraken die voor elk bedrijf gelden ("AI maakt processen efficienter")
- Dingen die vandaag al bestaan en als toekomstvisie worden gepresenteerd
- Opsommingen of bullets — het moet een verhaal zijn
- Techno-utopisme dat de menselijke kern mist

**Genereer ook:**
- **PULL_QUOTE**: De slotquote van de persoon uit het verhaal, als blockquote. Formaat: `"[Quote]" — [Naam], [functie] bij [BEDRIJFSNAAM], 2035`
- **KERNGETALLEN**: Vier feitelijke highlights uit het verhaal. Kies getallen en feiten die echt in het verhaal voorkomen. Formaat per regel: `[emoji] **[getal of feit]** — [korte duiding]`. Kies passende emoji's op basis van het thema.

Sla op: TOEKOMSTVERHAAL, PULL_QUOTE, KERNGETALLEN

### 5E — Gebrandde toekomstvisie-afbeelding genereren

Input: BEDRIJFSNAAM, SECTOR, MERKIDENTITEIT, TOEKOMSTVERHAAL (beschikbaar na 5D)

**Belangrijk:** 5E wacht op 5D (het toekomstverhaal) en op 5A (in Cowork gebruiken beide dezelfde browser-tab). Start 5E pas als zowel 5D als 5A klaar zijn. In Cowork: hergebruik dezelfde tab als 5A maar gebruik `window._geminiB64_visie` en `window._geminiMime_visie` als variabelen (niet dezelfde als 5A).

Schrijf een gedetailleerde Engelse prompt voor Gemini image generation. De afbeelding moet onmiskenbaar van dit bedrijf zijn. Verwerk altijd:
- **Merkkleur(en)** als dominant kleuraccent (gebruik hex-codes uit MERKIDENTITEIT)
- **Kenmerkende visuele elementen** van het merk: logo op kleding/voertuigen, herkenbare uniformen, gebouwen of materialen
- **Tagline of wordmark** subtiel maar zichtbaar in de scene
- **Sfeer passend bij de merkidentiteit**: warm/zakelijk/technisch afhankelijk van MERKIDENTITEIT

Aanvullende eisen:
- **Stijl**: hyperrealistisch, fotografisch, 8K, cinematische diepte
- **Persoon centraal**: een herkenbare medewerker in beeld, niet abstract
- **Natuur + technologie + bedrijf in synergie**: natuur aanwezig maar ondersteunend (groene daken, plantenwand, zonlicht door bomen)
- **Geen cliches**: geen robotarmen, blauwe hologrammen, Matrix-visuals, stockfoto-poses

Genereer de afbeelding via dezelfde methode als 5A (omgevingsdetectie: lokaal via curl, Cowork via browser MCP). Gebruik het Gemini model `gemini-3-pro-image-preview`.

**Fallback:** Als generatie faalt, gebruik placeholder: `https://ui-avatars.com/api/?name=[BEDRIJFSNAAM]+2035&size=400&background=1a1a2e&color=e94560&bold=true&format=png`

**Diagnostics:** `[DIAG 5E] Visie-afbeelding: [methode gebruikt] → [URL of FAIL]`

Sla op: VISIE_IMAGE_URL

---

## Stap 6: Notion-pagina aanmaken

Wacht tot 5A, 5B, 5C, 5D en 5E klaar zijn.

### Notion Markdown — verplichte syntax

De content MOET Notion-flavored markdown gebruiken:
- Afbeeldingen: `![Caption](URL)` (NIET `<image>` tags)
- Tabellen: `<table>` XML, cellen ALLEEN rich text (geen images/blocks)
- Kolommen: `<columns><column>` met children ingesprongen via tabs `</column></columns>`
- Callouts: `::: callout {icon="emoji"}\ntekst\n:::`
- To-do's: `- [ ] tekst`
- Haal NOOIT apart de Notion markdown spec op via ReadMcpResourceTool

### 6A — Klantpagina aanmaken

Gebruik `notion-create-pages`.

De `parent` parameter is optioneel: laat weg voor workspace-niveau, of geef een `page_id` mee als je de pagina onder een bestaande pagina wilt plaatsen.

**Paginatitel:** Gebruik `AI Panda x [BEDRIJFSNAAM]` als paginatitel.

**Foto's:** Als foto_url leeg is → gebruik `https://ui-avatars.com/api/?name=[VOORNAAM]&size=150&background=2EA3F2&color=ffffff&bold=true&rounded=true`

**Datum:** Gebruik formaat "DD maand YYYY" (bijv. "17 februari 2026").

### Content template (AI Panda huisstijl):

```markdown
![AI Panda x [BEDRIJFSNAAM] — Jouw AI-traject]([PANDA_IMAGE_URL])

# AI Panda x [BEDRIJFSNAAM]

*Jouw persoonlijke AI-trajectpagina — [DATUM]*

---

<callout icon="💬">**"[PULL_QUOTE]"**</callout>

---

## Over [BEDRIJFSNAAM]

[OMSCHRIJVING]

**Sector:** [SECTOR] | **Website:** [WEBSITE_DOMEIN]

---

## Jouw Toekomstvisie: [BEDRIJFSNAAM] in 2035

[TOEKOMSTVERHAAL]

![[BEDRIJFSNAAM] in 2035 — AI-toekomstvisie]([VISIE_IMAGE_URL])

<columns>
	<column>
[KERNGETAL_1]
	</column>
	<column>
[KERNGETAL_2]
	</column>
	<column>
[KERNGETAL_3]
	</column>
	<column>
[KERNGETAL_4]
	</column>
</columns>

---

## Jouw AI Panda Team

<columns>
	<column>
		![[NAAM_1]]([FOTO_URL_1])
		**[NAAM_1]**
		[FUNCTIE_1]
		[TELEFOON_1]
		[EMAIL_1]
	</column>
	<column>
		![[NAAM_2]]([FOTO_URL_2])
		**[NAAM_2]**
		[FUNCTIE_2]
		[TELEFOON_2]
		[EMAIL_2]
	</column>
	<column>
		![[NAAM_3]]([FOTO_URL_3])
		**[NAAM_3]**
		[FUNCTIE_3]
		[TELEFOON_3]
		[EMAIL_3]
	</column>
</columns>

*Heb je een vraag? Stuur gerust een berichtje via het emailadres hierboven.*

---

## AI Implementatie Roadmap

Hieronder vind je de roadmap die specifiek is opgesteld voor [BEDRIJFSNAAM] in de [SECTOR]-sector. Elke fase bouwt voort op de vorige.

<callout icon="🔍">**Fase 1 — Discovery** *(Week 1-2)*

[ROADMAP_FASE_1]</callout>

<callout icon="🧪">**Fase 2 — Pilot** *(Week 3-6)*

[ROADMAP_FASE_2]</callout>

<callout icon="🚀">**Fase 3 — Implementatie** *(Week 7-12)*

[ROADMAP_FASE_3]</callout>

<callout icon="📈">**Fase 4 — Schaling & Optimalisatie** *(Week 13+)*

[ROADMAP_FASE_4]</callout>

---

## Volgende Stappen

- [ ] Kickoff meeting plannen met [BEDRIJFSNAAM]
- [ ] Toegang tot relevante data en systemen regelen
- [ ] Discovery-interviews inplannen met key stakeholders
- [ ] Eerste AI-kansen rapport opleveren aan directie

---

## AI-Readiness Quickscan

Ontdek in 2 minuten hoe ver [BEDRIJFSNAAM] staat met AI. Beantwoord 5 korte vragen en krijg direct je profiel.

<embed source="[QUIZ_URL]">AI-Readiness Quickscan voor [BEDRIJFSNAAM]</embed>

[Start de AI-Readiness Quickscan]([QUIZ_URL])

| Score | Profiel | Wat dit betekent |
|---|---|---|
| 5-7 | De Starter | Focus op bewustwording en laaghangend fruit. |
| 8-9 | De Verkenner | Tijd voor structuur en strategie. |
| 10-11 | De Groeier | Klaar voor serieuze pilot-projecten. |
| 12-13 | De Versneller | Opschalen van successen naar bedrijfsbreed. |
| 14-15 | De Koploper | Focus op innovatie en voorsprong. |

---

*Gegenereerd door AI Panda Cowork — [DATUM]*
```

**Dynamische team-sectie:** Genereer zoveel `<column>` blokken als er geselecteerde consultants zijn. Het template hierboven toont 3 als voorbeeld, maar pas dit aan op het werkelijke aantal.

**Quiz embed:** Het template bevat zowel een `<embed>` blok als een tekstlink voor de quiz. Als Notion de embed niet ondersteunt (GitHub Pages URL niet in whitelist), wordt de link automatisch als fallback getoond. Verwijder de `<embed>` tag als je weet dat het niet werkt, zodat er geen lege embed op de pagina staat.

**Sla het `id` uit de response op als KLANTPAGINA_ID** (UUID met dashes, bijv. `abc123-...`).

---

## Stap 7: Bevestig het resultaat

Toon:
1. Klantpagina aangemaakt
2. Klantpagina: `[KLANTPAGINA_URL]` (klikbaar)
3. Interactieve quiz: `[QUIZ_URL]` (klikbaar)
4. Korte samenvatting: bedrijf, toekomstvisie (met pull quote preview), consultants, roadmap en interactieve quiz gegenereerd
5. Geef de visie-afbeelding prompt weer zodat de gebruiker die kan beoordelen

---

## Foutafhandeling

De skill moet ALTIJD een Notion-pagina opleveren. Geen enkele fout mag de flow stoppen:
- WebSearch faalt → gebruiker vragen
- Merkidentiteit niet gevonden → gebruik generieke waarden (donkerblauw, zakelijke stijl) en meld dit
- Sectorprobleem niet gevonden via WebSearch → gebruik eigen kennis over de sector, meld dit
- Excel niet gevonden → namen gebruiken zoals ingetypt
- Panda-afbeelding generatie faalt → placeholder URL, doorgaan
- Toekomstverhaal generatie faalt → schrijf een korter verhaal (150-200 woorden) als fallback
- Visie-afbeelding generatie faalt → placeholder URL, doorgaan
- Notion parent faalt → pagina zonder parent aanmaken
- Quiz base64-encoding faalt → Python fallback gebruiken
- Quiz-URL te lang → vraagteksten verkorten
