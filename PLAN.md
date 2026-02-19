# AI Panda Klantpagina

## Doel
Een Claude Code plugin die het aanmaken van professionele Notion-klantpagina's voor AI Panda automatiseert. Van bedrijfsnaam tot complete pagina met bedrijfsinfo, AI-gegenereerde afbeelding, teamleden en een sector-specifieke roadmap. De gebruiker hoeft alleen een bedrijf en consultatennamen op te geven en te bevestigen — de rest gaat automatisch.

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
- **Component review:** alle 10 klantpagina-componenten doorgelopen en verbeterd:
  - Hero image caption verwijderd, 0x0.st als primaire uploadhost
  - Subtitel verwijderd
  - Toekomstvisie (verhaal + kerngetallen + visie-afbeelding) verwijderd (gaat naar Gamma.app)
  - 2028 medewerker-quote toegevoegd als opening callout
  - Twee-koloms layout: "Over Klant" + "Over AI Panda" naast elkaar
  - Telefoon toegevoegd uit Excel voor teamleden
  - "Volgende Stappen" to-do sectie verwijderd (intern gebruik)
  - Quiz van link naar `<video>` embed gewijzigd
  - MCP server: `upload_to_0x0` als primair, catbox.moe als fallback

### Openstaand
- Toekomstvisie-presentatie via Gamma.app integreren
- Prompt Optimizer valideren en finetunen (Marnix)
- Onboarding documentatie voor medestudenten (Marnix)
- Branch protection instellen op main (Marnix)

## Architectuur

### Overzicht
Het project is een Claude Code plugin bestaande uit skills (Markdown workflows), Python scripts (beeldgeneratie) en een MCP server (Gemini beeldgeneratie). De plugin orkestreert MCP-servers (Notion, Gemini) voor een end-to-end workflow.

### UX-flow (gebruikersperspectief)

```
Gebruiker geeft bedrijfsnaam/URL op
  -> Gebruiker typt consultatennamen
  -> [parallel] Bedrijfsinfo ophalen + Excel matchen
  -> Bevestigingsscherm: klopt dit?
  -> [parallel] AI-afbeelding genereren + content voorbereiden
  -> Image uploaden -> Notion-pagina aanmaken
  -> Notion-URL teruggeven
```

### Stappen en parallelisatie

**Invoerfase (sequentieel, gebruiker input vereist):**
1. Bedrijfsnaam of URL invoeren
2. Consultatennamen typen (open veld)

**Ophaalfase (parallel starten na stap 2):**
- A: WebFetch/WebSearch -> bedrijfsnaam, omschrijving, sector
- B: Python-script -> Excel lezen, getypte namen matchen aan teamleden

**Bevestigingsfase:**
3. Toon samenvatting: bedrijfsinfo + gematchte consultants
4. Gebruiker bevestigt of past aan

**Uitvoerfase (parallel na bevestiging):**
- C: Gemini -> AI-afbeelding genereren
- D: Roadmap-content samenstellen (geen externe call)

**Afrondingsfase (sequentieel):**
5. Afbeelding uploaden naar catbox.moe
6. Notion-pagina aanmaken met alle content
7. Notion-URL tonen

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
│   ├── klantpagina/SKILL.md              # Hoofdskill: klantpagina generator
│   ├── ai-quiz/SKILL.md                  # Standalone AI-Readiness quiz skill
│   └── gemini-image/SKILL.md             # Standalone image generation skill
├── assets/panda-reference.png            # Panda character referentiebeeld
├── data/ai-panda-team.xlsx               # Teambestand met consultants
├── docs/                                 # Referentiemateriaal en verslagen
├── quiz/                                 # Interactieve quiz app (git submodule → aipanda-quiz)
├── scripts/
│   ├── generate_notion_image.py          # Nano Banana Pro beeldgeneratie
│   ├── prompt-optimizer.py               # Prompt templates voor Gemini
│   └── banana.sh                         # CLI wrapper
├── plugin/                               # Plugin bronbestanden
│   ├── .claude-plugin/plugin.json        # Plugin metadata
│   ├── .mcp.json                         # MCP server configuratie
│   ├── commands/klantpagina.md           # /klantpagina slash command
│   ├── hooks/hooks.json                  # Kwaliteitscheck hook
│   ├── servers/gemini-image-server.py    # Gemini MCP server
│   └── skills/klantpagina/SKILL.md      # Skill (gesynct vanuit .claude/)
├── build.sh                              # Bouwt plugin/ tot .zip
└── ai-panda-klantpagina.zip              # Gebouwd plugin-bestand
```

## Stack & Koppelingen

### Services
| Service | Doel | Koppeling |
|---|---|---|
| Google Gemini | AI-beeldgeneratie | MCP server + Python SDK |
| Notion | Klantpagina's aanmaken | MCP Server (notion-create-pages) |
| 0x0.st | Tijdelijke image hosting (primair) | cURL upload |
| catbox.moe | Tijdelijke image hosting (fallback) | cURL upload |
| Cloudinary | Image hosting (optioneel) | Python SDK |

### Environment Variables
| Variabele | Doel | Verplicht |
|---|---|---|
| GEMINI_API_KEY | Google Gemini API | Ja |
| CLOUDINARY_CLOUD_NAME | Cloudinary account | Nee |
| CLOUDINARY_API_KEY | Cloudinary authenticatie | Nee |
| CLOUDINARY_API_SECRET | Cloudinary secret | Nee |

## Infrastructuur
- Geen eigen hosting: draait lokaal als Claude Code plugin
- Distributie via plugin-bestand (`ai-panda-klantpagina.zip`)
- Git repository: MarnieX/AiPanda-Klantpagina
