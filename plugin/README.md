# AI Panda Klantpagina Generator

Genereer professionele Notion-klantpagina's voor AI Panda met een interactieve wizard.

## Wat doet deze plugin?

De plugin begeleidt je stap voor stap bij het aanmaken van een klantpagina in Notion:

1. Vraagt voor welk bedrijf de pagina is
2. Haalt automatisch bedrijfsinformatie op van de website
3. Leest het AI Panda teambestand (Excel) in
4. Laat je consultants kiezen voor dit project
5. Genereert een gepersonaliseerde AI Panda mascotte-afbeelding via Google Gemini
6. Maakt een complete Notion-pagina aan met bedrijfsprofiel, team en AI-roadmap
7. Checkt automatisch of de pagina aan alle kwaliteitseisen voldoet

## Componenten

| Component | Naam | Beschrijving |
|-----------|------|-------------|
| Skill | `klantpagina` | Volledige wizard-instructies |
| Command | `/klantpagina` | Snelle trigger om de wizard te starten |
| MCP Server | `gemini-images` | Beeldgeneratie via Google Gemini API |
| Hook | Kwaliteitscheck | Controleert automatisch of de pagina compleet en specifiek is |

## Setup

### Vereist

- **Notion-connector** in Cowork (voor het aanmaken van pagina's)
- **ai-panda-team.xlsx** in je werkmap (Excel met teamleden)

### Google Gemini API (voor afbeeldingen)

Stel je Gemini API key in als environment variable:

```
GEMINI_API_KEY=jouw-api-key-hier
```

Je kunt dit doen via een `.env` bestand of door de key in te stellen in je systeemomgeving.

Zonder API key werkt de plugin nog steeds, maar gebruikt dan een placeholder-afbeelding.

### Python-afhankelijkheden

De MCP server installeert automatisch:
- `mcp[cli]` (MCP framework)
- `httpx` (HTTP client)
- `openpyxl` (Excel-lezer, voor de skill)

## Gebruik

### Via slash command
Typ `/klantpagina` en volg de wizard.

### Via natuurlijke taal
Zeg iets als "maak een klantpagina voor Coolblue" en de skill wordt automatisch getriggerd.

## Excel-formaat (ai-panda-team.xlsx)

| Kolom A | Kolom B | Kolom C | Kolom D | Kolom E | Kolom F |
|---------|---------|---------|---------|---------|---------|
| Naam | Functie | Team | Foto URL | (overig) | Email |
