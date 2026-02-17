# AI Panda Klantpagina

## Doel
Een Claude Code plugin die het aanmaken van professionele Notion-klantpagina's voor AI Panda automatiseert. Van bedrijfsnaam tot complete pagina met bedrijfsinfo, teamleden, AI-gegenereerde afbeelding en sector-specifieke roadmap.

## Features

### Afgerond ✅
- (nog geen afgeronde features)

### In ontwikkeling 🚧
- (nog geen features in ontwikkeling)

### Gepland 📋
- Klantpagina skill: geautomatiseerde flow van klantnaam naar Notion-pagina
- Nano Banana Pro: AI-beeldgeneratie via Google Gemini
- Prompt Optimizer: automatische prompt-optimalisatie voor beeldgeneratie
- Team-integratie: consultants inlezen uit Excel en koppelen aan klantpagina
- Fallback-systeem: elke stap heeft een fallback zodat de flow nooit stopt
- Plugin packaging en distributie voor Cowork

## Architectuur

### Overzicht
Het project is een Claude Code plugin bestaande uit skills (Markdown workflows), Python scripts (beeldgeneratie) en shell scripts (CLI wrappers). De plugin orkestreert MCP-servers (Notion, Gemini) om een end-to-end workflow uit te voeren.

### Data Flow
1. Gebruiker start `/klantpagina` in Claude Code
2. Skill vraagt om bedrijfsnaam
3. WebFetch/WebSearch haalt bedrijfsinfo op
4. Excel wordt gelezen voor teamleden
5. Gebruiker selecteert consultants
6. Gemini genereert panda-afbeelding met bedrijfsnaam
7. Afbeelding wordt geüpload naar catbox.moe
8. Notion MCP maakt de klantpagina aan met alle verzamelde data

## Stack & Koppelingen

### Services
| Service | Doel | Koppeling |
|---|---|---|
| Google Gemini | AI-beeldgeneratie | API via Python SDK + MCP |
| Notion | Klantpagina's aanmaken | MCP Server |
| Cloudinary | Image hosting (optioneel) | API via Python SDK |
| Catbox.moe | Tijdelijke image hosting | cURL upload |

### Environment Variables
| Variabele | Doel | Geconfigureerd in |
|---|---|---|
| GEMINI_API_KEY | Google Gemini API | .env |
| CLOUDINARY_CLOUD_NAME | Cloudinary account | .env |
| CLOUDINARY_API_KEY | Cloudinary authenticatie | .env |
| CLOUDINARY_API_SECRET | Cloudinary secret | .env |

## Infrastructuur
- Geen eigen hosting: draait lokaal als Claude Code plugin
- Distributie via plugin-bestand (`ai-panda-klantpagina.plugin`)
- Git repository op GitHub: MarnieX/AiPanda-Klantpagina
