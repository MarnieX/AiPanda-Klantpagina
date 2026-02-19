---
name: klantpagina-v2
description: "Genereer een professionele Notion-klantpagina voor AI Panda. Orchestreert sub-skills voor image-generatie, quiz en toekomstvisie. Leest team uit Excel via MCP en gebruikt een extern template."
---

# AI Panda Klantpagina Generator v2

Je genereert een professionele Notion-klantpagina voor AI Panda. Volg de stappen exact in volgorde. Start parallelstappen altijd tegelijk om snelheid te winnen.

Gebruik TodoWrite om voortgang te tonen:
1. Bedrijfsnaam ophalen + API key checken
2. Bedrijfsinfo + Excel laden (parallel)
3. Consultants selecteren
4. Bevestiging vragen
5. Panda-afbeelding + roadmap + quiz-URL + 2028-quote (parallel)
6. Notion-pagina aanmaken
7. Toon Notion-URL + Quiz-URL direct
8. Toekomstvisie presentatie genereren (Gamma, na de finish)

---

## Stap 1: Vraag om bedrijf

Vraag de gebruiker: "Voor welk bedrijf wil je een klantpagina maken? Geef de bedrijfsnaam of website-URL."

Gebruik hiervoor GEEN AskUserQuestion (dat vereist opties). Stel de vraag als gewone tekst en wacht op het antwoord.

Sla op: KLANT_INPUT (naam of URL zoals ingetypt door gebruiker)

### Gemini API key check (parallel met wachten op antwoord)

Controleer of de Gemini API key beschikbaar is via de MCP tool `check_gemini_api_key`.

**Als `available: false`:** Vraag de key via AskUserQuestion:
- question: "GEMINI_API_KEY ontbreekt. Die heb ik nodig om een panda-afbeelding te genereren. Plak je Gemini API key hieronder (aanmaken op https://aistudio.google.com/apikey)."
- header: "API Key"
- options:
  - "Ik heb geen key, sla de afbeelding over (Recommended)" — ga door zonder image
  - "Key komt eraan" — de gebruiker plakt de key via het Other-tekstveld
- multiSelect: false

Als de gebruiker een key plakt: sla deze op via de MCP tool `set_gemini_api_key` met de geplakte key. Dit maakt de key beschikbaar voor de hele sessie (alleen in geheugen, niet op schijf). Exporteer de key ook in de shell voor eventuele curl-fallbacks:
```bash
export GEMINI_API_KEY="[GEPLAKTE_KEY]"
```

**Als `available: true`:** Key is al beschikbaar, ga door.

---

## Stap 2: Parallel ophalen (2A + 2B tegelijk)

### 2A — Bedrijfsinfo ophalen

Gebruik WebSearch met query: `"[klant] Nederland bedrijf sector omschrijving"`

Als KLANT_INPUT een URL of domein bevat, gebruik dat als WEBSITE_DOMEIN. Anders, leid het domein af uit de WebSearch-resultaten.

Fallback: als WebSearch geen bruikbare resultaten oplevert, gebruik de naam zoals ingetypt, omschrijving leeg laten voor bevestigingsstap.

Sla op: BEDRIJFSNAAM, OMSCHRIJVING, SECTOR, WEBSITE_DOMEIN (bijv. `bol.com`, zonder https://)

### 2B — Excel lezen via MCP

Gebruik de MCP tool `read_team_excel` om alle teamleden op te halen.

Parse de JSON-response:
- Array → sla op als ALLE_TEAMLEDEN
- Object met `error` → ga door zonder teamdata (fallback in stap 3)

Fallback als MCP tool niet beschikbaar of faalt: ga door zonder teamdata, vraag namen handmatig in stap 3. GA ALTIJD DOOR.

---

## Stap 3: Consultants selecteren

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
```

Gebruik daarna AskUserQuestion:
- question: "Klopt bovenstaande informatie, of wil je iets aanpassen?"
- header: "Bevestiging"
- options:
  - "Ziet er goed uit, ga door (Recommended)"
  - "Bedrijfsinfo aanpassen"
  - "Consultants aanpassen"

Als de gebruiker wil aanpassen: vraag wat er anders moet en verwerk de correctie. Herhaal het bevestigingsscherm daarna niet opnieuw.

---

## Stap 5: Parallel uitvoeren (5A + 5B + 5C + 5D tegelijk)

### 5A — AI Panda-afbeelding genereren

Voer de `gemini-image-v2` skill uit in quick mode.

Bouw een beschrijvende Engelse prompt op basis van BEDRIJFSNAAM, SECTOR en WEBSITE_DOMEIN. Voorbeeld:
```
A friendly cartoon red panda mascot in a navy blue business polo shirt
with "[BEDRIJFSNAAM]" embroidered on the chest, standing confidently
in a modern office presenting AI solutions on a whiteboard.
Professional illustration, clean white background.
```

Geef IMAGE_PROMPT mee en volg de stappen van gemini-image-v2 vanaf stap 2 (API key check). Het resultaat is IMAGE_URL (publieke URL of lege string).

**Laatste fallback — AI Studio pakket:**

Als alle automatische methodes zijn mislukt, toon het volgende pakket aan de gebruiker:

---
**Genereer de afbeelding zelf in Google AI Studio** — https://aistudio.google.com/

**Model:** `gemini-3-pro-image-preview`
**Output type:** Image generation
**Prompt** (kopieer dit): `[DE OPGEBOUWDE PANDA_PROMPT]`
**Referentieafbeelding (optioneel):** `https://files.catbox.moe/23dzti.png`

---

Gebruik daarna AskUserQuestion:
- question: "Afbeelding kon niet automatisch worden gegenereerd. Plak hieronder een URL als je hem al hebt, of ga door zonder afbeelding."
- header: "Afbeelding"
- options:
  - "Ga door, ik voeg de afbeelding zelf toe in Notion (Recommended)"
  - "Ik heb een URL" (gebruiker plakt via Other-veld)

Als URL geplakt: gebruik die als PANDA_IMAGE_URL.
Als "ga door": PANDA_IMAGE_URL = lege string (afbeeldingsregel wordt weggelaten in template).

### 5B — Roadmap content voorbereiden

Bereid de sector-specifieke roadmap voor (geen externe call nodig):

Maak elke fase specifiek voor SECTOR en BEDRIJFSNAAM. Vermijd generieke tekst. Voorbeelden per sector:
- Retail/e-commerce → productaanbevelingen, voorraadbeheer, vraagvoorspelling
- Zorg → patiëntmonitoring, planningsoptimalisatie, medische beeldherkenning
- Logistiek → routeoptimalisatie, voorspellend onderhoud, warehouse-automatisering
- Fintech → fraudedetectie, risicobeoordeling, chatbot-automatisering
- B2B/dienstverlening → offerteautomatisering, kennismanagement, CRM-verrijking

Sla op als ROADMAP_CONTENT (markdown tekst voor fase 1 t/m 4).

### 5C — Interactieve quiz genereren

Voer de `ai-quiz-v2` skill uit in quick mode.

Geef mee: BEDRIJFSNAAM, SECTOR, PARENT_SKILL = "klantpagina-v2"

Volg de stappen van ai-quiz-v2 vanaf stap 1 (vragen genereren). Stap 4 (Notion-pagina) wordt overgeslagen door PARENT_SKILL.

Het resultaat is QUIZ_URL.

### 5D — Medewerker-quote 2028 genereren

Genereer een korte, pakkende quote (1-2 zinnen) van een fictieve medewerker van [BEDRIJFSNAAM], die beschrijft hoe hun werk er radicaal anders uitziet in 2028 dankzij AI.

**Instructies:**
1. Kies een realistische functietitel die past bij de sector (geen CEO/directeur, maar iemand op de werkvloer)
2. Beschrijf iets specifieks dat vandaag nog handmatig/tijdrovend is, maar in 2028 door AI wordt gedaan
3. Eindig met een terloopse vergelijking met "hoe het vroeger was"
4. Toon: nuchter, niet overdreven enthousiast, alsof het de normaalste zaak van de wereld is
5. Max 2 zinnen

**Formaat:** `"[Quote]" — [Voornaam], [functie] bij [BEDRIJFSNAAM], 2028`

Sla op: MEDEWERKER_QUOTE

---

## Stap 6: Notion-pagina aanmaken

Wacht tot 5A, 5B, 5C en 5D klaar zijn.

### 6A — Template lezen en invullen

Lees het template uit `plugin/templates/klantpagina.md` (zoek via `CLAUDE_PLUGIN_ROOT/templates/klantpagina.md` of relatief pad).

Vervang alle `[VARIABELE]` placeholders met werkelijke waarden. Volg de instructies in het template voor:
- Dynamische team-kolommen (zoveel `<column>` blokken als consultants)
- Foto's (fallback naar ui-avatars als foto_url leeg)
- Afbeelding weglaten als PANDA_IMAGE_URL leeg
- Datum in formaat "DD maand YYYY"

### 6B — Pre-validatie

Controleer de ingevulde content voordat je de Notion API aanroept:
- Geen lege `![]()` afbeeldingen
- Alle callouts gebruiken `:::` syntax (niet HTML)
- Alle kolommen hebben tab-ingesprongen children
- Geen `[VARIABELE]` placeholders meer over

### 6C — Notion-pagina aanmaken

Gebruik `notion-create-pages`.

De `parent` parameter is optioneel: laat weg voor workspace-niveau, of geef een `page_id` mee als je de pagina onder een bestaande pagina wilt plaatsen.

**Paginatitel:** `AI Panda x [BEDRIJFSNAAM]`

**Sla het `id` uit de response op als KLANTPAGINA_ID.**

---

## Stap 7: Bevestig het resultaat (direct na Notion)

Toon **zodra de Notion-pagina aangemaakt is**:

```
Klantpagina klaar voor [BEDRIJFSNAAM]!

Notion-klantpagina: [KLANTPAGINA_URL]
Interactieve quiz:  [QUIZ_URL]

Toekomstvisie presentatie wordt nu gegenereerd...
```

---

## Stap 8: Toekomstvisie presentatie genereren (Gamma)

Voer dit uit NADAT de Notion-URL getoond is in stap 7.

Voer de `ai-toekomstvisie-v2` skill uit in quick mode.

Geef mee: BEDRIJFSNAAM, SECTOR, OMSCHRIJVING (verzameld in stap 2A).

Volg de stappen van ai-toekomstvisie-v2 vanaf stap 1 (research).

Zodra klaar, toon:

```
Toekomstvisie presentatie:  [GAMMA_URL]
```

---

## Foutafhandeling

De skill moet ALTIJD een Notion-pagina opleveren. Geen enkele fout mag de flow stoppen:
- WebSearch faalt → gebruiker vragen
- Excel niet gevonden / MCP tool faalt → namen handmatig vragen
- Panda-afbeelding generatie faalt → lege string, regel weglaten
- Medewerker-quote generatie faalt → gebruik generieke quote, doorgaan
- Notion parent faalt → pagina zonder parent aanmaken
- Quiz base64-encoding faalt → Python fallback gebruiken
- Quiz-URL te lang → vraagteksten verkorten
- Gamma generatie faalt → toon outline als Markdown, ga door
