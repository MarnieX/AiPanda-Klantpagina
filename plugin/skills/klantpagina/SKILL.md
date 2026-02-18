---
name: klantpagina
description: "Genereer een professionele Notion-klantpagina voor AI Panda. Haalt bedrijfsinfo op van de website, leest consultants uit een Excel, genereert een AI Panda-afbeelding en maakt een complete Notion-pagina met roadmap."
---

# AI Panda Klantpagina Generator

Je genereert een professionele Notion-klantpagina voor AI Panda. Volg de stappen exact in volgorde. Start parallelstappen altijd tegelijk om snelheid te winnen.

Gebruik TodoWrite om voortgang te tonen:
1. Bedrijfsnaam ophalen
2. Bedrijfsinfo + Excel laden (parallel)
3. Consultants selecteren
4. Bevestiging vragen
5. Afbeelding, roadmap + quizvragen voorbereiden (parallel)
6. Notion-pagina + quiz sub-pagina aanmaken

---

## Stap 1: Vraag om bedrijf

Vraag de gebruiker: "Voor welk bedrijf wil je een klantpagina maken? Geef de bedrijfsnaam of website-URL."

Gebruik hiervoor GEEN AskUserQuestion (dat vereist opties). Stel de vraag als gewone tekst en wacht op het antwoord.

Sla op: KLANT_INPUT (naam of URL zoals ingetypt door gebruiker)

---

## Stap 2: Parallel ophalen (start beide tegelijk)

### 2A — Bedrijfsinfo ophalen

Als KLANT_INPUT een URL bevat (http of een domein), gebruik WebFetch direct op die URL.
Anders, bouw de URL op als `https://www.[klant].nl` of zoek via WebSearch.

WebFetch prompt: "Geef in het Nederlands: 1) Officiële bedrijfsnaam, 2) Omschrijving in 2-3 zinnen (wat doet het bedrijf, sector, wat maakt het uniek), 3) De sector in één woord"

Fallback: als WebFetch faalt (403/timeout) → WebSearch met query "[klant] Nederland bedrijfsprofiel"
Fallback 2: als beide falen → gebruik de naam zoals ingetypt, omschrijving leeg laten voor bevestigingsstap

**Diagnostics:** Meld altijd welke methode gebruikt is:
- `[DIAG 2A] WebFetch geslaagd op [URL]`
- `[DIAG 2A] WebFetch faalde (403/timeout) → WebSearch gebruikt`
- `[DIAG 2A] WebSearch ook gefaald → handmatige invoer`

Sla op: BEDRIJFSNAAM, OMSCHRIJVING, SECTOR, WEBSITE_DOMEIN (bijv. `bol.com`, zonder https://)

### 2B — Excel lezen (alle teamleden laden)

Gebruik `find` als primaire zoekmethode (betrouwbaarder dan hardcoded paden in Cowork):

```bash
pip install openpyxl --break-system-packages -q 2>/dev/null

echo "[DIAG 2B] Zoeken naar ai-panda-team.xlsx via find /sessions ~ (maxdepth 10)..."
EXCEL_PATH=$(find /sessions ~ -maxdepth 10 -name "ai-panda-team.xlsx" 2>/dev/null | head -1)

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

## Stap 5: Parallel uitvoeren (start alle drie tegelijk na bevestiging)

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

In Cowork blokkeert de sandbox-proxy uitgaand HTTP-verkeer. Gebruik de Chrome MCP-bridge.

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

**5A-C.4 — Upload naar catbox.moe voor publieke URL:**
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

Als `success: true`: de URL is PANDA_IMAGE_URL.

**Als CORS blokkeert:** Navigeer naar `https://catbox.moe` en voer upload uit als same-origin request (gebruik `/user/api.php` als pad). **Let op:** na navigatie gaat `window._geminiB64` verloren. Sla de base64 data daarom op in een lokale variabele of voer generatie + upload op dezelfde pagina uit.

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
  Browser JS fetch (Gemini API) → Catbox upload vanuit browser → Publieke URL
  Als catbox CORS faalt: navigeer naar catbox.moe → same-origin upload
  Laatste fallback: Placeholder URL
```

**Diagnostics:** Meld altijd welke methode gebruikt is:
- `[DIAG 5A] Lokaal: Python script geslaagd`
- `[DIAG 5A] Lokaal: curl-fallback gebruikt`
- `[DIAG 5A] Cowork: browser MCP flow geslaagd`
- `[DIAG 5A] Cowork: catbox CORS fallback gebruikt`
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

### 5C — Quizvragen genereren

Input: BEDRIJFSNAAM, SECTOR (beschikbaar na stap 2A)

Genereer 5 sector-specifieke meerkeuzevragen. Volg exact dezelfde instructies als in `.claude/skills/ai-quiz/SKILL.md` stap 1.

**Structuur per vraag:**
- Vraagstelling (Bold)
- 3 Antwoordopties (A/B/C) oplopend in volwassenheid (A=Start, B=Groei, C=Leider)

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

Sla op als QUIZ_VRAGEN (markdown met 5 vragen, A/B/C per vraag).

---

## Stap 6: Notion-pagina + quiz sub-pagina aanmaken

Wacht tot 5A, 5B en 5C klaar zijn.

### Notion Markdown — verplichte syntax

De content MOET Notion-flavored markdown gebruiken:
- Afbeeldingen: `<image source="URL">caption</image>` (NIET `![alt](url)`)
- Tabellen: `<table>` XML, cellen ALLEEN rich text (geen images/blocks)
- Kolommen: `<columns><column>...</column></columns>`
- Callouts: `<callout icon="emoji">tekst</callout>`
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
<image source="[PANDA_IMAGE_URL]">AI Panda x [BEDRIJFSNAAM] — Jouw AI-traject</image>

# AI Panda x [BEDRIJFSNAAM]

*Jouw persoonlijke AI-trajectpagina — [DATUM]*

---

<callout icon="💬">**"Wij bouwen aan 7-sterren organisaties: effectiever, efficienter en leuker."** — AI Panda</callout>

---

## Over [BEDRIJFSNAAM]

[OMSCHRIJVING]

**Sector:** [SECTOR] | **Website:** [WEBSITE_DOMEIN]

---

## De AI Panda Aanpak

<columns>
	<column>
### Effectiever
Betere besluiten, snellere processen en slimmere samenwerking met AI als copiloot voor jouw team.
	</column>
	<column>
### Efficienter
Routinewerk automatiseren zodat jij en je collega's tijd overhouden voor wat echt telt.
	</column>
	<column>
### Leuker
AI neemt het saaie uit je werk. Meer energie voor creativiteit, groei en echte impact.
	</column>
</columns>

---

## Jouw AI Panda Team

<columns>
	<column>
<image source="[FOTO_URL_1]">[NAAM_1]</image>

**[NAAM_1]**
[FUNCTIE_1]
[EMAIL_1]
	</column>
	<column>
<image source="[FOTO_URL_2]">[NAAM_2]</image>

**[NAAM_2]**
[FUNCTIE_2]
[EMAIL_2]
	</column>
	<column>
<image source="[FOTO_URL_3]">[NAAM_3]</image>

**[NAAM_3]**
[FUNCTIE_3]
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

## Handige Links & Kennisbronnen

- [AI Panda website](https://aipanda.nl) — Meer weten over onze aanpak?
- [Snel contact via WhatsApp](https://aipanda.nl/afspraakbevestigd/) — Direct een vraag stellen
- [AI in het MKB](https://aipanda.nl/ai-in-het-mkb/) — Hoe AI jouw sector verandert
- Contact: info@aipanda.nl

---

## AI-Readiness Quickscan

Wil je weten hoe ver jouw organisatie staat met AI? Beantwoord 5 korte vragen en ontdek je AI-volwassenheidsniveau op de schaal van starter tot koploper.

Open de sub-pagina **AI-Readiness Quickscan** hieronder om te starten.

---

## Het 7-Sterren AI-Maturity Model

AI Panda werkt met zeven niveaus van AI-volwassenheid. Hoe hoger jouw ster, hoe beter je organisatie AI inzet om te groeien, te besparen en te vernieuwen.

| Niveau | Naam | Wat betekent dit? |
|---|---|---|
| 1 | Onbewust | Geen bewustzijn van AI-mogelijkheden in de organisatie |
| 2 | Bewust | Bekend met AI, maar nog geen actief gebruik |
| 3 | Experimenterend | Eerste experimenten met AI-tools door vroege adopters |
| 4 | Structureel | AI structureel ingezet in dagelijkse processen |
| 5 | Strategisch | AI als strategisch concurrentievoordeel ingezet |
| 6 | AI-gedreven | De organisatie is volledig AI-first ingericht |
| 7 | Meester | Meester in het ontwikkelen en implementeren van AI |

*Het doel van dit traject: [BEDRIJFSNAAM] naar een structureel hoger niveau tillen.*

---

*Gegenereerd door AI Panda Cowork — [DATUM]*
```

**Dynamische team-sectie:** Genereer zoveel `<column>` blokken als er geselecteerde consultants zijn. Het template hierboven toont 3 als voorbeeld, maar pas dit aan op het werkelijke aantal.

**Sla het `id` uit de response op als KLANTPAGINA_ID** (UUID met dashes, bijv. `abc123-...`).

### 6B — Quiz sub-pagina aanmaken

Tool: `notion-create-pages`
- Parent: `page_id: KLANTPAGINA_ID`
- Titel: `AI-Readiness Quickscan — [BEDRIJFSNAAM]`
- Content (vervang [QUIZ_VRAGEN] met de volledige markdown uit stap 5C):

```markdown
# AI-Readiness Quickscan

Vul deze korte scan in om te ontdekken waar jullie staan op het gebied van AI.
Bespreek de antwoorden tijdens de kickoff met het AI Panda team.

---

[QUIZ_VRAGEN]

---

## Score-indicatie

| Je antwoorden | Profiel | Wat dit betekent |
|---|---|---|
| Vooral A | De Starter | Jullie staan aan het begin. Focus nu op bewustwording en laaghangend fruit. |
| Mix van A & B | De Verkenner | De interesse is er en er zijn losse tools. Tijd voor structuur en strategie. |
| Vooral B | De Groeier | De basis staat. Jullie zijn klaar voor serieuze pilot-projecten en data-integratie. |
| Mix van B & C | De Versneller | Jullie gaan hard. De uitdaging is nu: opschalen van losse successen naar bedrijfsbreed. |
| Vooral C | De Koploper | AI zit in jullie DNA. Focus op innovatie en het voorblijven van de concurrentie. |

---

*Vul je antwoorden in via de database hieronder. Je profiel verschijnt automatisch.*
```

**Sla het `id` uit de response op als QUIZ_PAGE_ID.**

### 6C — Quiz database aanmaken

Tool: `notion-create-database`
- Parent: `page_id: QUIZ_PAGE_ID`
- Titel: `Jouw antwoorden`
- Properties:
  - `Naam` — type: title
  - `V1 - AI gebruik` — type: select, opties: `A`, `B`, `C`
  - `V2 - Data` — type: select, opties: `A`, `B`, `C`
  - `V3 - Automatisering` — type: select, opties: `A`, `B`, `C`
  - `V4 - Team` — type: select, opties: `A`, `B`, `C`
  - `V5 - Strategie` — type: select, opties: `A`, `B`, `C`
  - `Score /15` — type: formula, expression:
    ```
    toNumber(if(prop("V1 - AI gebruik") == "C", "3", if(prop("V1 - AI gebruik") == "B", "2", "1"))) + toNumber(if(prop("V2 - Data") == "C", "3", if(prop("V2 - Data") == "B", "2", "1"))) + toNumber(if(prop("V3 - Automatisering") == "C", "3", if(prop("V3 - Automatisering") == "B", "2", "1"))) + toNumber(if(prop("V4 - Team") == "C", "3", if(prop("V4 - Team") == "B", "2", "1"))) + toNumber(if(prop("V5 - Strategie") == "C", "3", if(prop("V5 - Strategie") == "B", "2", "1")))
    ```
  - `Profiel` — type: formula, expression:
    ```
    if(prop("Score /15") >= 14, "De Koploper", if(prop("Score /15") >= 12, "De Versneller", if(prop("Score /15") >= 10, "De Groeier", if(prop("Score /15") >= 8, "De Verkenner", "De Starter"))))
    ```

**Fallback als formula-properties niet ondersteund worden:** Maak de database aan zonder `Score /15` en `Profiel`, en voeg een callout toe aan de sub-pagina met tekst: "Tel je score: A=1, B=2, C=3. Totaal 5-7 = Starter, 8-9 = Verkenner, 10-11 = Groeier, 12-13 = Versneller, 14-15 = Koploper."

**Sla het `id` uit de response op als QUIZ_DB_ID.**

### 6D — Pre-fill eerste rij

Tool: `notion-create-pages`
- Parent: `database_id: QUIZ_DB_ID`
- Properties: `Naam` = `[BEDRIJFSNAAM]`

---

## Stap 7: Bevestig het resultaat

Toon:
1. Klantpagina aangemaakt
2. Klantpagina: `[KLANTPAGINA_URL]` (klikbaar)
3. Quiz sub-pagina: `[QUIZ_PAGE_URL]` (klikbaar)
4. Korte samenvatting: bedrijf, consultants, roadmap en quiz gegenereerd

---

## Foutafhandeling

De skill moet ALTIJD een Notion-pagina opleveren. Geen enkele fout mag de flow stoppen:
- WebFetch faalt → WebSearch → gebruiker vragen
- Excel niet gevonden → namen gebruiken zoals ingetypt
- Image-generatie faalt → placeholder URL, doorgaan
- Notion parent faalt → pagina zonder parent aanmaken
- Quiz sub-pagina aanmaken faalt → doorgaan zonder, meld het resultaat
- Database formula niet ondersteund → database zonder formules met callout als fallback
- Stap 6B/6C/6D falen → klantpagina alsnog tonen als eindresultaat
