---
name: klantpagina
description: "Genereer een professionele Notion-klantpagina voor AI Panda. Haalt bedrijfsinfo op, leest consultants uit een Excel, genereert een AI Panda-afbeelding en maakt een complete Notion-pagina met roadmap en interactieve quiz."
---

# AI Panda Klantpagina Generator

Je genereert een professionele Notion-klantpagina voor AI Panda. Volg de stappen exact in volgorde. Start parallelstappen altijd tegelijk om snelheid te winnen.

Gebruik TodoWrite om voortgang te tonen:
1. Bedrijfsnaam ophalen
2. Bedrijfsinfo + Excel laden (parallel)
3. Consultants selecteren
4. Bevestiging vragen
5. Panda-afbeelding + roadmap + quiz-URL + 2028-quote (parallel)
6. Notion-pagina aanmaken (quiz als embed)

---

## Stap 1: Vraag om bedrijf

Vraag de gebruiker: "Voor welk bedrijf wil je een klantpagina maken? Geef de bedrijfsnaam of website-URL."

Gebruik hiervoor GEEN AskUserQuestion (dat vereist opties). Stel de vraag als gewone tekst en wacht op het antwoord.

Sla op: KLANT_INPUT (naam of URL zoals ingetypt door gebruiker)

---

## Stap 2: Parallel ophalen (2A + 2B tegelijk)

### 2A — Bedrijfsinfo ophalen

Gebruik WebSearch met query: `"[klant] Nederland bedrijf sector omschrijving"`

Als KLANT_INPUT een URL of domein bevat, gebruik dat als WEBSITE_DOMEIN. Anders, leid het domein af uit de WebSearch-resultaten.

Fallback: als WebSearch geen bruikbare resultaten oplevert, gebruik de naam zoals ingetypt, omschrijving leeg laten voor bevestigingsstap.

**Diagnostics:** Meld altijd welke methode gebruikt is:
- `[DIAG 2A] WebSearch geslaagd`
- `[DIAG 2A] WebSearch gefaald → handmatige invoer`

Sla op: BEDRIJFSNAAM, OMSCHRIJVING, SECTOR, WEBSITE_DOMEIN (bijv. `bol.com`, zonder https://)

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
            "telefoon": entry.get("telefoon", ""),
            "email": entry.get("e-mail", entry.get("email", ""))
        })
print(f"[DIAG 2B] {len(team)} teamleden geladen", file=sys.stderr)
print(f"[DIAG 2B] Headers gevonden: {headers}", file=sys.stderr)
print(json.dumps(team, indent=2, ensure_ascii=False))
PYEOF
fi
```

Sla op: ALLE_TEAMLEDEN (volledige lijst met naam, functie, foto_url, telefoon, email per teamlid)

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

## Stap 5: Parallel uitvoeren (5A + 5B + 5C + 5D tegelijk)

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

# Upload naar 0x0.st (primair), catbox.moe (fallback)
PANDA_IMAGE_URL=$(curl -s -F "file=@$OUTPUT" https://0x0.st)
if [ -z "$PANDA_IMAGE_URL" ] || ! echo "$PANDA_IMAGE_URL" | grep -q "^http"; then
    PANDA_IMAGE_URL=$(curl -s -F "reqtype=fileupload" -F "fileToUpload=@$OUTPUT" https://catbox.moe/user/api.php)
fi
echo "[DIAG 5A] Curl-fallback URL: $PANDA_IMAGE_URL"
```

---

#### Cowork (ENVIRONMENT=cowork)

In Cowork blokkeert de sandbox-proxy uitgaand HTTP-verkeer voor directe Python/curl calls. Er zijn twee routes: de MCP server (primair, werkt nu dankzij socksio fix) en de Chrome MCP-bridge (fallback).

**Methode 1: MCP server tools (primair)**

Gebruik de MCP tool `generate_custom_image` of `generate_panda_image` (afhankelijk van context). Deze tools genereren de afbeelding via Gemini EN uploaden naar 0x0.st (primair) of catbox.moe (fallback), alles server-side (geen CORS-problemen).

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
  3. Browser JS fetch + browser upload naar 0x0.st (laatste poging)
  4. Placeholder URL
```

**Diagnostics:** Meld altijd welke methode gebruikt is:
- `[DIAG 5A] Lokaal: Python script geslaagd`
- `[DIAG 5A] Lokaal: curl-fallback gebruikt`
- `[DIAG 5A] Cowork: MCP generate_panda_image geslaagd`
- `[DIAG 5A] Cowork: browser + upload_image_base64 fallback gebruikt`
- `[DIAG 5A] Cowork: browser + 0x0.st browser upload gebruikt`
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

### 5D — Medewerker-quote 2028 genereren

Input: BEDRIJFSNAAM, SECTOR, OMSCHRIJVING (beschikbaar na stap 2A)

Genereer een korte, pakkende quote (1-2 zinnen) van een fictieve medewerker van [BEDRIJFSNAAM], die beschrijft hoe hun werk er radicaal anders uitziet in 2028 dankzij AI.

**Instructies:**
1. Kies een realistische functietitel die past bij de sector (geen CEO/directeur, maar iemand op de werkvloer)
2. Beschrijf iets specifieks dat vandaag nog handmatig/tijdrovend is, maar in 2028 door AI wordt gedaan
3. Eindig met een terloopse vergelijking met "hoe het vroeger was"
4. Toon: nuchter, niet overdreven enthousiast, alsof het de normaalste zaak van de wereld is
5. Max 2 zinnen

**Formaat:** `"[Quote]" — [Voornaam], [functie] bij [BEDRIJFSNAAM], 2028`

**Voorbeelden:**
- *Retail:* "Ik open 's ochtends mijn dashboard en zie dat het assortiment van drie filialen vannacht al is aangepast op basis van het weer en lokale evenementen. Vroeger was dat een weekproject." — Lisa, filiaalmanager bij Etos, 2028
- *Logistiek:* "Onze AI plant nu routes die ik na twintig jaar ervaring niet had bedacht. Ik besteed mijn tijd aan de uitzonderingen die echt een mens nodig hebben." — Marco, operations lead bij DHL, 2028

Sla op: MEDEWERKER_QUOTE

---

## Stap 6: Notion-pagina aanmaken

Wacht tot 5A, 5B, 5C en 5D klaar zijn.

### Notion Markdown — verplichte syntax

De content MOET Notion-flavored markdown gebruiken. Hieronder staat de volledige referentie:

**Afbeeldingen:**
```
![Caption](URL)
![](URL)              ← zonder caption (geen grijze tekst onder de afbeelding)
```

**Callouts (Pandoc-style fenced divs, NIET HTML-tags):**
```
::: callout {icon="emoji"}
Tekst en **rich text** hier
:::
```
FOUT: `<callout icon="emoji">tekst</callout>` — dit werkt NIET.

**Kolommen (children MOETEN met tabs ingesprongen):**
```
<columns>
	<column>
		![](URL)
		**Naam**
		Functie
	</column>
	<column>
		Content hier
	</column>
</columns>
```
FOUT: children zonder tab-inspringing worden niet gerenderd.

**Tabellen:** `<table>` XML, cellen ALLEEN rich text (geen images/blocks).

**To-do's:** `- [ ] tekst`

**Dividers:** `---`

**Toggle:**
```
<details>
<summary>Titel</summary>
	Children (ingesprongen)
</details>
```

**Embeds:** Notion heeft geen `<embed>` tag. Gebruik `<video src="URL">Caption</video>` om een URL te embedden (werkt ook voor niet-video content zoals webapps).

### 6A — Klantpagina aanmaken

Gebruik `notion-create-pages`.

De `parent` parameter is optioneel: laat weg voor workspace-niveau, of geef een `page_id` mee als je de pagina onder een bestaande pagina wilt plaatsen.

**Paginatitel:** Gebruik `AI Panda x [BEDRIJFSNAAM]` als paginatitel.

**Foto's:** Als foto_url leeg is → gebruik `https://ui-avatars.com/api/?name=[VOORNAAM]&size=150&background=2EA3F2&color=ffffff&bold=true&rounded=true`

**Datum:** Gebruik formaat "DD maand YYYY" (bijv. "17 februari 2026").

### Content template (AI Panda huisstijl):

```markdown
![]([PANDA_IMAGE_URL])

# AI Panda x [BEDRIJFSNAAM]

---

::: callout {icon="💬"}
**"[MEDEWERKER_QUOTE]"**
:::

---

<columns>
	<column>
		## Over [BEDRIJFSNAAM]
		[OMSCHRIJVING]
		**Sector:** [SECTOR]
		**Website:** [WEBSITE_DOMEIN]
	</column>
	<column>
		## Over AI Panda
		AI Panda begeleidt organisaties naar AI-volwassenheid. Geen technologie-eerst aanpak, maar mens-eerst: 80% van AI-succes zit in menselijk gedrag, 20% in technologie. Van strategie tot implementatie.
		**Tagline:** Making AI Work For You
		**Website:** aipanda.nl
	</column>
</columns>

---

## Jouw AI Panda Team

<columns>
	<column>
		![]([FOTO_URL_1])
		**[NAAM_1]**
		[FUNCTIE_1]
		[TELEFOON_1]
		[EMAIL_1]
	</column>
	<column>
		![]([FOTO_URL_2])
		**[NAAM_2]**
		[FUNCTIE_2]
		[TELEFOON_2]
		[EMAIL_2]
	</column>
	<column>
		![]([FOTO_URL_3])
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

::: callout {icon="🔍"}
**Fase 1 — Discovery** *(Week 1-2)*

[ROADMAP_FASE_1]
:::

::: callout {icon="🧪"}
**Fase 2 — Pilot** *(Week 3-6)*

[ROADMAP_FASE_2]
:::

::: callout {icon="🚀"}
**Fase 3 — Implementatie** *(Week 7-12)*

[ROADMAP_FASE_3]
:::

::: callout {icon="📈"}
**Fase 4 — Schaling & Optimalisatie** *(Week 13+)*

[ROADMAP_FASE_4]
:::

---

## AI-Readiness Quickscan

Ontdek in 2 minuten hoe ver [BEDRIJFSNAAM] staat met AI. Beantwoord 5 korte vragen en krijg direct je profiel.

<video src="[QUIZ_URL]">AI-Readiness Quickscan</video>

---

*Gegenereerd door AI Panda Cowork — [DATUM]*
```

**Dynamische team-sectie:** Genereer zoveel `<column>` blokken als er geselecteerde consultants zijn. Het template hierboven toont 3 als voorbeeld, maar pas dit aan op het werkelijke aantal.

**Quiz embed:** De quiz wordt als `<video>` embed getoond (Notion workaround voor non-video embeds).

**Sla het `id` uit de response op als KLANTPAGINA_ID** (UUID met dashes, bijv. `abc123-...`).

---

## Stap 7: Bevestig het resultaat

Toon:
1. Klantpagina aangemaakt
2. Klantpagina: `[KLANTPAGINA_URL]` (klikbaar)
3. Interactieve quiz: `[QUIZ_URL]` (klikbaar)
4. Korte samenvatting: bedrijf, 2028-quote, consultants, roadmap en interactieve quiz gegenereerd

---

## Foutafhandeling

De skill moet ALTIJD een Notion-pagina opleveren. Geen enkele fout mag de flow stoppen:
- WebSearch faalt → gebruiker vragen
- Excel niet gevonden → namen gebruiken zoals ingetypt
- Panda-afbeelding generatie faalt → placeholder URL, doorgaan
- Medewerker-quote generatie faalt → gebruik generieke quote, doorgaan
- Notion parent faalt → pagina zonder parent aanmaken
- Quiz base64-encoding faalt → Python fallback gebruiken
- Quiz-URL te lang → vraagteksten verkorten
