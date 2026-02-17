# MCP Image Server Installeren voor Cowork

## Wat is het?
De `mcp-image` MCP-server laat Cowork/Claude direct afbeeldingen genereren via Google Gemini. Geen Python-scripts meer nodig — het wordt een native tool die Claude kan aanroepen.

## Vereisten
- Node.js 20+ (check: `node --version`)
- Jouw Gemini API key (die heb je al: staat in `.env`)

## Stap 1: MCP-server toevoegen via Claude Code CLI

Open een terminal op je eigen machine en voer uit:

```bash
claude mcp add mcp-image \
  --env GEMINI_API_KEY=JOUW_API_KEY_HIER \
  --env IMAGE_OUTPUT_DIR=/tmp/mcp-images \
  -- npx -y mcp-image
```

Dit registreert de server zodat Claude/Cowork hem automatisch opstart.

## Stap 2: Verifieer de installatie

Start een nieuw Cowork-gesprek en typ:

```
Genereer een afbeelding van een panda met een Jumbo t-shirt
```

Als het werkt, zie je dat Claude de `generate_image` tool gebruikt.

## Stap 3: Test de volledige flow

Typ `/klantpagina` in Cowork en doorloop de hele flow. De Gemini-afbeelding zou nu automatisch moeten werken.

## Beschikbare tool: generate_image

Parameters:
- `prompt` (verplicht) — beschrijving van de gewenste afbeelding
- `aspectRatio` — "1:1", "3:4", "4:3", "9:16", "16:9"
- `imageSize` — "1K", "2K", "4K"
- `fileName` — naam voor het outputbestand

## Troubleshooting

**"Command not found: npx"**
→ Installeer Node.js: https://nodejs.org

**"GEMINI_API_KEY not set"**
→ Check of de key correct is meegegeven in het `claude mcp add` commando

**Server start niet op**
→ Test handmatig: `GEMINI_API_KEY=jouw-key npx -y mcp-image`

**Afbeelding wordt niet gegenereerd**
→ Check je Gemini API quota op https://aistudio.google.com
