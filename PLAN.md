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

### In ontwikkeling
- Notion-pagina template: strakke opmaak met AI Panda huisstijl

### Gepland
- Cloud Cowork uitlegpagina: aparte Notion-subpagina over het platform (Rick)
- AI-quiz skill: 5 vragen, sector-specifiek, bepaalt AI-niveau klant (Noud)
- Toekomstbeeld/AI-visie skill: gepersonaliseerd per bedrijf en sector (Rick)
- Plugin installatie testen in Cowork (Marnix)
- Onboarding documentatie voor medestudenten (Marnix)

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

1. Header-afbeelding (AI Panda x Bedrijf, gegenereerd door Gemini)
2. Over [Bedrijf]: omschrijving en sector
3. Jouw AI Panda Team: tabel met foto, naam, functie, contact
4. AI Implementatie Roadmap: 4 sector-specifieke fases
5. Volgende stappen: checklist voor kickoff
6. Over AI Panda Cowork: placeholder sectie (volledige subpagina volgt)

### Projectstructuur

```
/
├── .claude/skills/klantpagina/SKILL.md   # Canonical skill (development)
├── assets/panda-reference.png            # Panda character referentiebeeld
├── data/ai-panda-team.xlsx               # Teambestand met consultants
├── docs/                                 # Referentiemateriaal en verslagen
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
| catbox.moe | Tijdelijke image hosting | cURL upload |
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
