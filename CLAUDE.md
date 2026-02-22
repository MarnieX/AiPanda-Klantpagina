# AI Panda Klantpagina - Claude Code Instructies

## Stack & Tech

**Primary:**
- Python 3.8+ (image generation via Google Gemini)
- Claude Code Skills (.claude/skills/) voor workflow-orchestratie
- Notion MCP Server (pagina's aanmaken en beheren)
- Google Gemini API (AI-beeldgeneratie)
- Cloudinary (optioneel, image hosting)

**Project type:** Claude Code Plugin met skills en MCP-integraties.

**Bestanden:**
- `ai-panda-klantpagina.zip` - Gebouwd plugin-bestand voor Cowork
- `.claude/skills/klantpagina/SKILL.md` - Hoofdskill: klantpagina generator (orchestrator)
- `.claude/skills/ai-quiz/SKILL.md` - Sub-skill: AI-Readiness quiz
- `.claude/skills/gemini-image/SKILL.md` - Sub-skill: AI-beeldgeneratie
- `.claude/skills/ai-toekomstvisie/SKILL.md` - Sub-skill: Gamma-presentatie
- `data/ai-panda-team.xlsx` - Teambestand met consultants
- `plugin/` - Plugin bronbestanden (servers, commands, skills)
- `plugin/servers/panda-server.py` - MCP server (Gemini/OpenAI image gen + Excel)
- `quiz/` - Interactieve quiz app (git submodule, GitHub Pages)
- `assets/panda-reference.png` - Panda character referentiebeeld voor Gemini
- `build.sh` - Bouwt plugin/ tot .zip

## Patronen & Conventies

### Skill Structuur
Skills staan in `.claude/skills/[naam]/SKILL.md` en volgen het YAML frontmatter + Markdown format. Elke skill beschrijft stapsgewijs de workflow.

### MCP Integraties
- Notion: pagina's aanmaken via `notion-create-pages` (parent parameter werkt: gebruik `page_id` om onder een bestaande pagina aan te maken, of laat weg voor workspace-niveau)
- Gemini: beeldgeneratie via `generate_image` MCP tool of Python fallback
- Catbox.moe: tijdelijke image hosting via cURL upload

### Error Handling
De klantpagina-flow mag NOOIT stoppen op een fout. Elke stap heeft een fallback:
- WebFetch faalt → WebSearch → gebruiker vragen
- Image-generatie faalt → placeholder URL
- Excel niet gevonden → gebruiker vragen om namen

## Belangrijke Context

### External Services
- `GEMINI_API_KEY`: Google Gemini API (beeldgeneratie). Zie .env.example
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: Optioneel voor image hosting. Zie .env.example

### Team
Dit is een opleidingsproject bij AI Panda. Drie contributors werken samen aan dit project.

## Do's en Don'ts

### Do
- Volg de stappen in SKILL.md exact op volgorde
- Maak roadmap-fases specifiek per sector/bedrijf (geen generieke tekst)
- Gebruik fallbacks bij elke externe call
- Test skills lokaal voordat je commit

### Don't
- Commit nooit .env of API keys
- Stop nooit de klantpagina-flow bij een fout

## Overschrijvingen

**Dit project wijkt af van `~/.claude/CLAUDE.md` (globaal) op de volgende punten:**

- Geen overschrijvingen: globale regels (feature branches, commit conventies, Nederlands) gelden volledig
