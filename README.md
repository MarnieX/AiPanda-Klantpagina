# AI Panda - Klantpagina Generator

Toolset voor AI Panda (onderdeel van Marnit) om automatisch professionele Notion-klantpagina's te genereren, inclusief AI-gegenereerde afbeeldingen via Google Gemini.

## Wat zit erin?

### Nano Banana Pro (Image Pipeline)

Een pipeline om via Google Gemini afbeeldingen te genereren, optimaliseren en uploaden:

- **`prompt-optimizer.py`** - Neemt een simpele beschrijving en maakt er een geoptimaliseerde Gemini-prompt van. Ondersteunt stijlen: cartoon, foto, logo, artistiek.
- **`generate_notion_image.py`** - Genereert afbeeldingen via de Gemini API. Ondersteunt meerdere modellen, aspect ratio's en resoluties. Optioneel uploaden naar catbox.moe.
- **`nano-banana-generate.sh`** - One-click generator: voert het laatst gegenereerde prompt uit, accepteert directe prompts, of draait in watch-mode.
- **`banana.sh`** - De ultieme one-liner: combineert prompt-optimalisatie en image generatie in een enkel commando.

### Claude Code Skills

- **Klantpagina Skill** - Claude Code skill die bedrijfsinfo ophaalt van een website, consultants uit een Excel leest, een AI Panda-afbeelding genereert en een complete Notion-pagina aanmaakt met roadmap.

### MCP Server

- **`setup-nano-banana-mcp.sh`** - Configuratiescript om de Nano Banana Pro MCP server in te stellen voor Claude Desktop.
- **`ai-panda-klantpagina.plugin`** - Plugin package met MCP server, skills, commands en hooks.

## Installatie

```bash
# 1. Clone de repository
git clone https://github.com/MarnieX/AiPanda-Klantpagina.git

# 2. Kopieer .env.example naar .env en vul je keys in
cp .env.example .env

# 3. Installeer Python dependencies
pip install google-genai Pillow python-dotenv requests

# 4. (Optioneel) MCP server setup voor Claude Desktop
chmod +x setup-nano-banana-mcp.sh
./setup-nano-banana-mcp.sh
```

## Gebruik

```bash
# Simpel: prompt optimaliseren + genereren in een stap
./banana.sh "een panda die code schrijft"

# Met opties
./banana.sh "berglandschap bij zonsopgang" --stijl foto --ratio 16:9
./banana.sh "koffieshop logo" --stijl logo --tekst "Morning Brew"

# Alleen afbeelding genereren
python generate_notion_image.py "een panda in een bamboe bos" --upload

# Alleen prompt optimaliseren
python prompt-optimizer.py "een panda" --stijl cartoon
```

## Vereisten

- Python 3.8+
- Google Gemini API key ([aanmaken](https://aistudio.google.com/apikey))
- Node.js (voor MCP server setup)

## Configuratie

Maak een `.env` bestand aan op basis van `.env.example`:

```
GEMINI_API_KEY=jouw-gemini-api-key
```

## Licentie

Intern project van AI Panda / Marnit.
