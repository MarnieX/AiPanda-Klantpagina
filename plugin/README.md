# AI Panda Klantpagina Generator v2.2

Genereer professionele Notion-klantpagina's voor AI Panda met een interactieve wizard.

## Wat doet deze plugin?

De plugin begeleidt je stap voor stap bij het aanmaken van een klantpagina in Notion:

1. Vraagt voor welk bedrijf de pagina is
2. Checkt API keys (Gemini + OpenAI)
3. Haalt automatisch bedrijfsinformatie op via WebSearch
4. Leest het AI Panda teambestand (Excel) in via MCP
5. Laat je consultants kiezen voor dit project
6. Genereert een fotorealistische AI Panda afbeelding (Gemini met referentie-image + bedrijfslogo, OpenAI als fallback)
7. Bouwt een sector-specifieke AI-roadmap, interactieve quiz en 2028-quote
8. Maakt een complete Notion-pagina aan vanuit een template
9. Genereert een toekomstvisie presentatie via Gamma

## Componenten

| Component | Naam | Beschrijving |
|-----------|------|-------------|
| Skill | `klantpagina-v2` | Orchestrator die sub-skills aanstuurt |
| Skill | `gemini-image-v2` | Image generation (Gemini + OpenAI fallback) |
| Skill | `ai-quiz-v2` | Interactieve AI-Readiness quiz |
| Skill | `ai-toekomstvisie-v2` | Gamma.app presentatie |
| Command | `/klantpagina` | Snelle trigger om de wizard te starten |
| MCP Server | `panda-server` | Beeldgeneratie, logo ophalen, team Excel, API key management |

## Setup

### Vereist

- **Notion-connector** in Cowork (voor het aanmaken van pagina's)

### API Keys

| Key | Service | Hoe instellen | Verplicht |
|-----|---------|--------------|-----------|
| `GEMINI_API_KEY` | Google Gemini (primaire image gen) | `~/.claude/settings.json` of `.env` | Ja (of invoeren via sessie-prompt) |
| `OPENAI_API_KEY` | OpenAI (fallback image gen) | `~/.claude/settings.json` of `.env` | Nee |
| `LOGO_DEV_TOKEN` | Logo.dev (bedrijfslogo's) | Hardcoded in `.mcp.json` | Nee (al inbegrepen) |

Voorbeeld `~/.claude/settings.json`:
```json
{
  "env": {
    "GEMINI_API_KEY": "AIza...",
    "OPENAI_API_KEY": "sk-..."
  }
}
```

Zonder API keys werkt de plugin nog steeds, maar gebruikt dan een placeholder-afbeelding.

### Python-afhankelijkheden

De MCP server installeert automatisch:
- `mcp[cli]` (MCP framework)
- `httpx` + `httpcore[socks]` (HTTP client)
- `openpyxl` (Excel-lezer)

## Gebruik

### Via slash command
Typ `/klantpagina` en volg de wizard.

### Via natuurlijke taal
Zeg iets als "maak een klantpagina voor Coolblue" en de skill wordt automatisch getriggerd.

## Image generation fallback-keten

```
Gemini + referentie-image + bedrijfslogo (multimodal)
  → OpenAI gpt-image-1.5 (prompt-only)
    → Placeholder/fallback URL (flow stopt nooit)
```

## Excel-formaat (ai-panda-team.xlsx)

| Kolom A | Kolom B | Kolom C | Kolom D | Kolom E | Kolom F |
|---------|---------|---------|---------|---------|---------|
| Naam | Functie | Team | Foto URL | (overig) | Email |
