# AI Panda Klantpagina

## Doel
Een Claude Code plugin die het aanmaken van professionele Notion-klantpagina's voor AI Panda automatiseert. Van bedrijfsnaam tot complete pagina met bedrijfsinfo, AI-gegenereerde afbeelding, teamleden, sector-specifieke roadmap, interactieve quiz en Gamma-presentatie. De gebruiker hoeft alleen een bedrijf en consultatennamen op te geven en te bevestigen — de rest gaat automatisch.

## Features

### Afgerond
- Minimale plugin opzetten met basis skill-structuur
- Notion MCP koppeling: pagina aanmaken vanuit skill
- Nano Banana Pro: panda-afbeelding genereren via Gemini (--client mode)
- Team-integratie: consultants uit Excel inlezen (13 teamleden)
- End-to-end flow: van klantnaam tot Notion-pagina (bol.com getest)
- Fallback-systeem gedocumenteerd voor alle externe calls
- Plugin packaging voor Cowork via build.sh
- Klantpagina skill volledig uitgewerkt met logo compositing en lokale paden
- Notion-pagina template met strakke opmaak en AI Panda huisstijl (hero banner, teamtabel, roadmap, 9 secties)
- Interactieve AI-Readiness Quickscan: quiz als GitHub Pages app (JSON + base64 in URL), als `<video>` embed op klantpagina
- Standalone `ai-quiz` skill: genereert quiz JSON, bouwt klikbare URL, optioneel Notion-pagina
- Generieke `gemini-image` skill: standalone image generation via curl en browser MCP
- Browser MCP flow voor image generation in Cowork (omgevingsdetectie, Chrome MCP-bridge)
- Curl-fallback voor image generation (omzeilt httpx SOCKS proxy in Cowork)
- Consultantfoto's geupload en team Excel bijgewerkt met URL's
- WebSearch vervangt WebFetch in bedrijfsinfo-ophaalfase
- Component review: alle 10 klantpagina-componenten doorgelopen en verbeterd
- AI Toekomstvisie: Gamma.app presentatie van 10 slides met visionair transformatieverhaal
- **Plugin v2.0.0: volledige herbouw met orchestrator-architectuur**
  - klantpagina-v2: orchestrator (~220 regels, was 678) delegeert naar sub-skills via quick mode
  - gemini-image-v2: quick mode + fallback_url handling
  - ai-quiz-v2: quick mode + optionele Notion-pagina + Python-first base64
  - ai-toekomstvisie-v2: quick mode + inline kwaliteitscheck
  - MCP server hernoemd naar panda-server.py met `read_team_excel` tool
  - Notion template geëxtraheerd naar apart bestand
  - Hooks verwijderd (quality check niet meer nodig)
- **Plugin v2.1.0: OpenAI fallback, fotorealistische prompt, logo-integratie**
  - OpenAI `gpt-image-1.5` als fallback na Gemini rate limits
  - Panda referentie-image (multimodal) meegegeven aan Gemini voor stijlconsistentie
  - Bedrijfslogo ophalen via Logo.dev + Google Favicons, als extra referentie-image
  - Fotorealistische panda-prompt (zwart pak, oranje stropdas, furry paws)
  - Dubbele API key management via `check_api_keys` / `set_api_key` MCP tools
  - Upload: catbox.moe (primair) + tmpfiles.org (fallback), 0x0.st verwijderd
  - Logo API: Logo.dev (primair) + Google Favicons (fallback), Clearbit verwijderd

### Openstaand
- Prompt Optimizer valideren en finetunen (Marnix)
- Onboarding documentatie voor medestudenten (Marnix)
- Branch protection instellen op main (Marnix)
- v1 skills verwijderen na validatie van v2 in Cowork

## Architectuur

### Overzicht
Het project is een Claude Code plugin bestaande uit skills (Markdown workflows), Python scripts (beeldgeneratie) en een MCP server (Gemini beeldgeneratie + team Excel). De plugin orkestreert MCP-servers (Notion, Gemini, Gamma) voor een end-to-end workflow.

### v2 Architectuur (orchestrator-model)

```
/klantpagina command
    │
    ▼
klantpagina-v2 (orchestrator, ~220 regels)
    │
    ├── Stap 1: check_api_keys ──► panda-server.py (Gemini + OpenAI)
    ├── Stap 2B: read_team_excel ──► panda-server.py
    │
    ├── Stap 5A: generate_panda_image ──► panda-server.py
    │       └── Gemini (ref+logo) → OpenAI (prompt-only) → fallback
    │
    ├── Stap 5C: ai-quiz-v2 (quick mode, geen Notion-pagina)
    │       └── Base64 encode + URL bouwen
    │
    ├── Stap 6: Leest plugin/templates/klantpagina.md
    │       └── notion-create-pages (Notion MCP)
    │
    └── Stap 8: ai-toekomstvisie-v2 (quick mode)
            └── mcp__claude_ai_Gamma__generate (Gamma MCP)
```

Elke sub-skill werkt ook standalone (met interactieve vragen). Quick mode wordt alleen geactiveerd als de input-variabelen al beschikbaar zijn.

### UX-flow (gebruikersperspectief)

```
Gebruiker geeft bedrijfsnaam/URL op
  -> API key check (indien nodig: gebruiker voert key in)
  -> [parallel] Bedrijfsinfo ophalen + Excel laden via MCP
  -> Consultants selecteren
  -> Bevestigingsscherm: klopt dit?
  -> [parallel] AI-afbeelding + roadmap + quiz + 2028-quote
  -> Notion-pagina aanmaken vanuit template
  -> Notion-URL + Quiz-URL tonen
  -> Toekomstvisie presentatie genereren (Gamma, na de finish)
```

### Notion-pagina structuur

1. Hero-afbeelding (AI Panda x Bedrijf, gegenereerd door Gemini, geen caption)
2. Titel (AI Panda x Bedrijfsnaam)
3. 2028-quote: callout met fictieve medewerkerscitaat uit de toekomst
4. Twee kolommen: "Over [Bedrijf]" (omschrijving, sector, website) | "Over AI Panda" (missie, tagline, website)
5. Jouw AI Panda Team: consultants met foto, functie, telefoon en email in kolommen
6. AI Implementatie Roadmap: 4 sector-specifieke fases in callouts
7. AI-Readiness Quickscan: interactieve quiz als `<video>` embed

### Projectstructuur

```
/
├── .claude/skills/
│   ├── klantpagina-v2/SKILL.md          # v2 orchestrator
│   ├── gemini-image-v2/SKILL.md         # v2 image generation (quick mode)
│   ├── ai-quiz-v2/SKILL.md             # v2 quiz (quick mode)
│   ├── ai-toekomstvisie-v2/SKILL.md    # v2 Gamma presentatie (quick mode)
│   ├── klantpagina/SKILL.md            # v1 (behouden)
│   ├── ai-quiz/SKILL.md               # v1 (behouden)
│   ├── gemini-image/SKILL.md           # v1 (behouden)
│   └── ai-toekomstvisie/SKILL.md      # v1 (behouden)
├── assets/panda-reference.png           # Panda character referentiebeeld
├── data/ai-panda-team.xlsx              # Teambestand met consultants
├── docs/                                # Referentiemateriaal en verslagen
├── quiz/                                # Interactieve quiz app (git submodule → aipanda-quiz)
├── scripts/
│   ├── generate_notion_image.py         # Nano Banana Pro beeldgeneratie
│   ├── prompt-optimizer.py              # Prompt templates voor Gemini
│   └── banana.sh                        # CLI wrapper
├── plugin/                              # Plugin bronbestanden
│   ├── .claude-plugin/plugin.json       # Plugin metadata (v2.1.0)
│   ├── .mcp.json                        # MCP server configuratie (panda-server, env vars)
│   ├── commands/klantpagina.md          # /klantpagina slash command → v2 skill
│   ├── servers/panda-server.py          # MCP server (Gemini/OpenAI + logo + Excel + API keys)
│   ├── templates/klantpagina.md         # Notion-pagina template met placeholders
│   └── skills/                          # Skills (gesynct vanuit .claude/)
├── build.sh                             # Bouwt plugin/ tot .zip
└── ai-panda-klantpagina.zip             # Gebouwd plugin-bestand
```

## Stack & Koppelingen

### Services
| Service | Doel | Koppeling |
|---|---|---|
| Google Gemini | AI-beeldgeneratie (primair) | MCP server (panda-server.py), multimodal met referentie-images |
| OpenAI | AI-beeldgeneratie (fallback) | MCP server (panda-server.py), gpt-image-1.5 |
| Logo.dev | Bedrijfslogo ophalen | cURL, publishable key in .mcp.json |
| Google Favicons | Bedrijfslogo fallback | cURL, gratis, geen key |
| Notion | Klantpagina's aanmaken | MCP Server (notion-create-pages) |
| Gamma.app | Toekomstvisie presentatie | MCP Server (claude_ai_Gamma) |
| catbox.moe | Tijdelijke image hosting (primair) | cURL upload |
| tmpfiles.org | Tijdelijke image hosting (fallback) | cURL upload + /dl/ URL-conversie |

### Environment Variables
| Variabele | Doel | Verplicht |
|---|---|---|
| GEMINI_API_KEY | Google Gemini API | Ja (of invoeren via sessie-prompt) |
| OPENAI_API_KEY | OpenAI API (fallback image gen) | Nee (Gemini is primair) |
| LOGO_DEV_TOKEN | Logo.dev bedrijfslogo's | Nee (hardcoded publishable key in .mcp.json) |

## Infrastructuur
- Geen eigen hosting: draait lokaal als Claude Code plugin
- Distributie via plugin-bestand (`ai-panda-klantpagina.zip`)
- Git repository: MarnieX/AiPanda-Klantpagina
