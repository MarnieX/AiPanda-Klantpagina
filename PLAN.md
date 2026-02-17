# AI Panda Klantpagina

## Doel
Een Claude Code plugin die het aanmaken van professionele Notion-klantpagina's voor AI Panda automatiseert. Van bedrijfsnaam tot complete pagina met bedrijfsinfo, AI-gegenereerde afbeelding, teamleden en een sector-specifieke roadmap. De gebruiker hoeft alleen een bedrijf en consultatennamen op te geven en te bevestigen — de rest gaat automatisch.

## Features

### Afgerond ✅
- Minimale plugin opzetten met basis skill-structuur
- Notion MCP koppeling: pagina aanmaken vanuit skill
- Nano Banana Pro: panda-afbeelding genereren via Gemini (--client mode)
- Team-integratie: consultants uit Excel inlezen (13 teamleden)
- End-to-end flow: van klantnaam tot Notion-pagina (bol.com getest)
- Fallback-systeem gedocumenteerd voor alle externe calls
- Plugin packaging voor Cowork via build.sh

### In ontwikkeling 🚧
- Klantpagina skill herschreven met nieuwe UX-flow (bevestigingsscherm, parallelisatie)

### Gepland 📋
- Notion-pagina template: strakke opmaak met AI Panda huisstijl
- Cloud Cowork uitlegpagina: aparte Notion-subpagina over het platform (Rick)
- AI-quiz skill: 5 vragen, sector-specifiek, bepaalt AI-niveau klant (Noud)
- Toekomstbeeld/AI-visie skill: gepersonaliseerd per bedrijf en sector (Rick)
- Plugin installatie testen in Cowork (Marnix)
- Onboarding documentatie voor medestudenten (Marnix)

## Architectuur

### Overzicht
Het project is een Claude Code plugin bestaande uit skills (Markdown workflows), Python scripts (beeldgeneratie) en shell scripts (CLI wrappers). De plugin orkestreert MCP-servers (Notion, Gemini) voor een end-to-end workflow.

### UX-flow (gebruikersperspectief)

```
Gebruiker geeft bedrijfsnaam/URL op
→ Gebruiker typt consultatennamen
→ [parallel] Bedrijfsinfo ophalen + Excel matchen
→ Bevestigingsscherm: klopt dit?
→ [parallel] AI-afbeelding genereren + content voorbereiden
→ Image uploaden → Notion-pagina aanmaken
→ ✅ Notion-URL teruggeven
```

### Stappen en parallelisatie

**Invoerfase (sequentieel — gebruiker input vereist):**
1. Bedrijfsnaam of URL invoeren
2. Consultatennamen typen (open veld)

**Ophaalfase (parallel starten na stap 2):**
- A: WebFetch/WebSearch → bedrijfsnaam, omschrijving, sector
- B: Python-script → Excel lezen, getypte namen matchen aan teamleden

**Bevestigingsfase:**
3. Toon samenvatting: bedrijfsinfo + gematchte consultants
4. Gebruiker bevestigt of past aan

**Uitvoerfase (parallel na bevestiging):**
- C: Gemini → AI-afbeelding genereren
- D: Roadmap-content samenstellen (geen externe call)

**Afrondingsfase (sequentieel):**
5. Afbeelding uploaden naar catbox.moe
6. Notion-pagina aanmaken met alle content
7. Notion-URL tonen

### Notion-pagina structuur (huidige simpele versie)

De pagina is een eenvoudige voorbeeldpagina totdat het definitieve template klaar is. Secties:
1. Header-afbeelding (AI Panda x Bedrijf, gegenereerd door Gemini)
2. Over [Bedrijf] — omschrijving en sector
3. Jouw AI Panda Team — tabel met foto, naam, functie, contact
4. AI Implementatie Roadmap — 4 sector-specifieke fases
5. Volgende stappen — checklist voor kickoff
6. Over AI Panda Cowork — placeholder sectie (volledige subpagina volgt)

### Data Flow (technisch)

1. Gebruiker start `/klantpagina`
2. Skill vraagt bedrijfsnaam of URL
3. Skill vraagt consultatennamen (open tekstveld)
4. Parallel: WebFetch/WebSearch voor bedrijfsinfo + Python voor Excel-matching
5. Bevestigingsscherm getoond
6. Na bevestiging parallel: Gemini beeldgeneratie + roadmap content
7. Upload naar catbox.moe
8. Notion MCP maakt pagina aan
9. URL teruggegeven aan gebruiker

## Stack & Koppelingen

### Services
| Service | Doel | Koppeling |
|---|---|---|
| Google Gemini | AI-beeldgeneratie | Python SDK via generate_notion_image.py |
| Notion | Klantpagina's aanmaken | MCP Server (notion-create-pages) |
| catbox.moe | Tijdelijke image hosting | cURL upload (--upload flag in script) |
| Cloudinary | Image hosting (optioneel) | Python SDK |

### Environment Variables
| Variabele | Doel | Geconfigureerd in |
|---|---|---|
| GEMINI_API_KEY | Google Gemini API | .env |
| CLOUDINARY_CLOUD_NAME | Cloudinary account | .env (optioneel) |
| CLOUDINARY_API_KEY | Cloudinary authenticatie | .env (optioneel) |
| CLOUDINARY_API_SECRET | Cloudinary secret | .env (optioneel) |

## Infrastructuur
- Geen eigen hosting: draait lokaal als Claude Code plugin
- Distributie via plugin-bestand (`ai-panda-klantpagina.plugin`)
- Git repository: MarnieX/AiPanda-Klantpagina
