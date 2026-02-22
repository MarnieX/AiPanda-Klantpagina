---
name: klantpagina
description: "Genereer een professionele Notion-klantpagina voor AI Panda. Orchestreert sub-skills voor image-generatie, quiz en toekomstvisie. Leest team uit Excel via MCP en gebruikt een extern template."
---

# AI Panda Klantpagina Generator

Je genereert een professionele Notion-klantpagina voor AI Panda. Volg de stappen exact in volgorde. Start parallelstappen altijd tegelijk om snelheid te winnen.

Gebruik TodoWrite om voortgang te tonen:
1. API key check + bedrijf vragen
2. Bedrijfsinfo + Excel laden (parallel)
3. Consultants selecteren
4. Panda-afbeelding + roadmap + quiz-URL + 2028-quote (parallel)
5. Notion-pagina aanmaken
6. Toon Notion-URL + Quiz-URL direct
7. Toekomstvisie presentatie genereren (Gamma, na de finish)

---

## Fase 0: API key check (vóór alles)

Controleer of API keys beschikbaar zijn via de MCP tool `check_api_keys`.

**Response:** `{"gemini": true/false, "openai": true/false}`

**Als minstens één key `true`:** Ga stil door.

**Als beide `false`:** Vraag de key via AskUserQuestion:
- question: "Geen API keys gevonden. Die heb ik nodig om een panda-afbeelding te genereren. Plak een Gemini of OpenAI API key hieronder. Gemini: https://aistudio.google.com/apikey — OpenAI: https://platform.openai.com/api-keys"
- header: "API Key"
- options:
  - "Ik heb geen key, sla de afbeelding over (Recommended)" — ga door zonder image
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

**Als de gebruiker geen key heeft:** Ga door zonder image. Stop NOOIT de flow.

---

## Fase 1: Minimale input (2 vragen, sequentieel)

### Vraag 1 — Bedrijf

Vraag de gebruiker: "Voor welk bedrijf maak ik een klantpagina? (naam of website-URL)"

Gebruik hiervoor GEEN AskUserQuestion (dat vereist opties). Stel de vraag als gewone tekst en wacht op het antwoord.

Sla op: KLANT_INPUT (naam of URL zoals ingetypt door gebruiker)

**Parallel na vraag 1 (onzichtbaar voor gebruiker):**
- WebSearch naar bedrijf → probeer sector + omvang te bepalen (zie fase 2A)
- Excel laden via `read_team_excel` (zie fase 2B)

### Vraag 1b — Sector/omvang (conditioneel)

Sla deze vraag over als de sector én bedrijfsomvang automatisch bepaald zijn via WebSearch.

Alleen stellen als het bedrijf onbekend of onduidelijk is:

Gebruik AskUserQuestion:
- question: "Ik kan [KLANT_INPUT] niet automatisch vinden. In welke sector is dit bedrijf actief?"
- header: "Sector"
- options:
  - "Retail / e-commerce"
  - "Zorg / medisch"
  - "Logistiek / transport"
  - "Fintech / financiële diensten"
  - "B2B / professionele dienstverlening"
  - "Overig" (gebruiker typt zelf via Other)
- multiSelect: false

### Vraag 2 — Consultants (zodra Excel klaar)

Wacht tot de `read_team_excel` call uit de parallelstap klaar is, dan stel deze vraag.

**Bij 4 of minder teamleden:** Gebruik AskUserQuestion met multiSelect:
- question: "Welke consultants werken aan dit traject?"
- header: "Team"
- multiSelect: true
- options: dynamisch opgebouwd uit ALLE_TEAMLEDEN, bijv:
  - label: "Marnix", description: "Project Lead"
  - label: "Noud", description: "Developer"

**Bij 5 of meer teamleden:** Toon een genummerde lijst van alle teamleden en stel een open tekstvraag: "Welke consultants werken aan dit traject? Typ de nummers of namen gescheiden door komma's."

**Fallback als Excel niet gevonden:** Stel een open tekstvraag: "Welke consultants werken aan dit traject? Typ de namen gescheiden door komma's."

Sla op: CONSULTANTS (lijst met naam, functie, foto_url, email per geselecteerde consultant, gematcht aan ALLE_TEAMLEDEN)

> Na vraag 2: geen verdere vragen aan de gebruiker. Alles loopt automatisch door.

---

## Fase 2: Parallel research (volledig automatisch)

Zodra vraag 2 beantwoord is, start alles tegelijk:

### 2A — Bedrijfsinfo ophalen

Gebruik WebSearch met query: `"[klant] Nederland bedrijf sector omschrijving"`

Als KLANT_INPUT een URL of domein bevat, gebruik dat als WEBSITE_DOMEIN. Anders, leid het domein af uit de WebSearch-resultaten.

Fallback: als WebSearch geen bruikbare resultaten oplevert, gebruik de naam zoals ingetypt.

Sla op: BEDRIJFSNAAM, OMSCHRIJVING, SECTOR, WEBSITE_DOMEIN (bijv. `bol.com`, zonder https://)

**Huisstijl ophalen (direct na WebSearch, als WEBSITE_DOMEIN bekend is):**

Doe een WebFetch op `https://[WEBSITE_DOMEIN]` en extraheer:
- **MERKKLEUR_PRIMAIR** — de dominante merkkleur als hex-code (bijv. `#E63329`)
- **MERKKLEUR_SECUNDAIR** — de tweede merkkleur als hex-code (bijv. `#1A1A1A`)
- **HUISSTIJL_KENMERK** — één typisch visueel kenmerk dat het merk onderscheidt (bijv. "vetgedrukte sans-serif typografie met veel witruimte")

Fallback als WebFetch faalt of geen kleuren zichtbaar zijn:
- MERKKLEUR_PRIMAIR = `#F97316` (AI Panda oranje)
- MERKKLEUR_SECUNDAIR = `#000000`
- HUISSTIJL_KENMERK = leeg string

**Sla alle zeven waarden op:** BEDRIJFSNAAM, OMSCHRIJVING, SECTOR, WEBSITE_DOMEIN, MERKKLEUR_PRIMAIR, MERKKLEUR_SECUNDAIR, HUISSTIJL_KENMERK

### 2B — Excel lezen via MCP

Gebruik de MCP tool `read_team_excel` om alle teamleden op te halen.

Parse de JSON-response:
- Array → sla op als ALLE_TEAMLEDEN
- Object met `error` → ga door zonder teamdata (fallback in vraag 2)

Fallback als MCP tool niet beschikbaar of faalt: ga door zonder teamdata. GA ALTIJD DOOR.

### 2C — AI Panda-afbeelding genereren

Gebruik de MCP tool `generate_panda_image` met alle beschikbare parameters:

```
MCP tool: generate_panda_image
  bedrijfsnaam: "[BEDRIJFSNAAM]"
  sector: "[SECTOR]"
  website: "[WEBSITE_DOMEIN]"
```

De tool bouwt intern een fotorealistische prompt, haalt het bedrijfslogo op via het domein, en probeert Gemini (met referentie-image + logo) → OpenAI (prompt-only) → fallback.

Parse de JSON-response:
- `success: true` → `image_url` is PANDA_IMAGE_URL
- `success: false` + `fallback_url` → gebruik `fallback_url` als PANDA_IMAGE_URL
- `success: false` zonder `fallback_url` → PANDA_IMAGE_URL = lege string (afbeeldingsregel weggelaten in template)

**Stop NOOIT de flow bij een mislukte afbeelding. Vraag NOOIT om een URL aan de gebruiker.**

### 2D — Roadmap content voorbereiden

Bereid de sector-specifieke roadmap voor (geen externe call nodig):

Maak elke fase specifiek voor SECTOR en BEDRIJFSNAAM. Vermijd generieke tekst. Voorbeelden per sector:
- Retail/e-commerce → productaanbevelingen, voorraadbeheer, vraagvoorspelling
- Zorg → patiëntmonitoring, planningsoptimalisatie, medische beeldherkenning
- Logistiek → routeoptimalisatie, voorspellend onderhoud, warehouse-automatisering
- Fintech → fraudedetectie, risicobeoordeling, chatbot-automatisering
- B2B/dienstverlening → offerteautomatisering, kennismanagement, CRM-verrijking

Sla op als ROADMAP_CONTENT (markdown tekst voor fase 1 t/m 4).

### 2E — Interactieve quiz genereren

Voer de `ai-quiz` skill uit in quick mode.

Geef mee: BEDRIJFSNAAM, SECTOR, PARENT_SKILL = "klantpagina"

Volg de stappen van ai-quiz vanaf stap 1 (vragen genereren). Stap 4 (Notion-pagina) wordt overgeslagen door PARENT_SKILL.

Het resultaat is QUIZ_URL.

### 2F — Medewerker-quote 2028 genereren

Genereer een korte, pakkende quote (1-2 zinnen) van een fictieve medewerker van [BEDRIJFSNAAM], die beschrijft hoe hun werk er radicaal anders uitziet in 2028 dankzij AI.

**Instructies:**
1. Kies een realistische functietitel die past bij de sector (geen CEO/directeur, maar iemand op de werkvloer)
2. Beschrijf iets specifieks dat vandaag nog handmatig/tijdrovend is, maar in 2028 door AI wordt gedaan
3. Eindig met een terloopse vergelijking met "hoe het vroeger was"
4. Toon: nuchter, niet overdreven enthousiast, alsof het de normaalste zaak van de wereld is
5. Max 2 zinnen

**Formaat:** `"[Quote]" — [Voornaam], [functie] bij [BEDRIJFSNAAM], 2028`

Sla op: MEDEWERKER_QUOTE

Wacht tot 2A + 2C + 2D + 2E + 2F klaar zijn.

---

## Fase 3: Notion-pagina aanmaken (automatisch)

### 3A — Template lezen en invullen

Lees het template uit `plugin/templates/klantpagina.md` (zoek via `CLAUDE_PLUGIN_ROOT/templates/klantpagina.md` of relatief pad).

Vervang alle `[VARIABELE]` placeholders met werkelijke waarden. Volg de instructies in het template voor:
- Dynamische team-kolommen (zoveel `<column>` blokken als consultants)
- Foto's (fallback naar ui-avatars als foto_url leeg)
- Afbeelding weglaten als PANDA_IMAGE_URL leeg
- Datum in formaat "DD maand YYYY"

### 3B — Pre-validatie

Controleer de ingevulde content voordat je de Notion API aanroept:
- Geen lege `![]()` afbeeldingen
- Alle callouts gebruiken `:::` syntax (niet HTML)
- Alle kolommen hebben tab-ingesprongen children
- Geen `[VARIABELE]` placeholders meer over

### 3C — Notion-pagina aanmaken

Gebruik `notion-create-pages`.

De `parent` parameter is optioneel: laat weg voor workspace-niveau, of geef een `page_id` mee als je de pagina onder een bestaande pagina wilt plaatsen.

**Paginatitel:** `AI Panda x [BEDRIJFSNAAM]`

**Sla het `id` uit de response op als KLANTPAGINA_ID.**

---

## Fase 3 — Resultaat tonen (direct na Notion)

Toon **zodra de Notion-pagina aangemaakt is**:

```
Klantpagina klaar voor [BEDRIJFSNAAM]!

Notion-klantpagina: [KLANTPAGINA_URL]
Interactieve quiz:  [QUIZ_URL]

Toekomstvisie presentatie wordt nu gegenereerd...
```

---

## Fase 4: Toekomstvisie genereren (automatisch, na Notion)

Voer dit uit NADAT de Notion-URL getoond is.

Voer de `ai-toekomstvisie` skill uit in quick mode.

Geef mee: BEDRIJFSNAAM, SECTOR, OMSCHRIJVING, WEBSITE_DOMEIN, MERKKLEUR_PRIMAIR,
MERKKLEUR_SECUNDAIR, HUISSTIJL_KENMERK (alle uit fase 2A).

Door deze variabelen mee te geven slaat ai-toekomstvisie stap 1A (huisstijl-research)
automatisch over, omdat de data al beschikbaar is. Dit bespaart een extra WebFetch-ronde.

Volg de stappen van ai-toekomstvisie vanaf stap 1 (research).

Zodra klaar, toon het eindresultaat:

```
Alles klaar voor [BEDRIJFSNAAM]!

Notion-klantpagina: [KLANTPAGINA_URL]
Interactieve quiz:  [QUIZ_URL]
Toekomstvisie:      [GAMMA_URL]
```

---

## Foutafhandeling

De skill moet ALTIJD een Notion-pagina opleveren. Geen enkele fout mag de flow stoppen:
- WebSearch faalt → gebruik naam zoals ingetypt, ga door
- Excel niet gevonden / MCP tool faalt → namen handmatig vragen in vraag 2
- Panda-afbeelding generatie faalt → lege string, regel weglaten in template
- Medewerker-quote generatie faalt → gebruik generieke quote, doorgaan
- Notion parent faalt → pagina zonder parent aanmaken
- Quiz base64-encoding faalt → Python fallback gebruiken
- Quiz-URL te lang → vraagteksten verkorten
- Gamma generatie faalt → toon outline als Markdown, ga door
