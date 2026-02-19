# Changelog

Alle noemenswaardige wijzigingen aan dit project worden hier gedocumenteerd.

Format gebaseerd op [Keep a Changelog](https://keepachangelog.com/nl/1.1.0/).
Dit project volgt [Semantic Versioning](https://semver.org/lang/nl/).

## [Unreleased]

*Geen wijzigingen.*

## [0.2.0] - 2026-02-18

Features uitgebouwd: toekomstvisie, interactieve quiz, browser MCP image generation, gemini-image skill.

### Added
- Toekomstvisie geintegreerd in klantpagina-skill: persoonlijke pull quote (vervangt generieke 7-sterren quote), 10-jaar transformatieverhaal (350-500 woorden visionair proza), gebrandde toekomstvisie-afbeelding via Gemini, en 4 kerngetallen
- Research-fase uitgebreid met merkidentiteit (kleuren, tagline, visuele stijl) en sectorprobleem-identificatie
- Kwaliteitscheck uitgebreid met toekomstverhaal, kerngetallen, visie-afbeelding en pull quote validatie
- Browser MCP flow voor image generation in Cowork: automatische omgevingsdetectie, Chrome MCP-bridge voor Gemini API calls via `tabs_context_mcp`, `navigate`, `javascript_tool` en `computer` (screenshot)
- Catbox.moe upload vanuit browser JS (Cowork): gegenereerde afbeeldingen uploaden voor publieke URL zonder sandbox-restricties
- Panda-reference.png permanent gehost op catbox.moe (`https://files.catbox.moe/23dzti.png`)
- `gemini-image` skill: generieke standalone image generation via curl en Nano Banana Pro (nano-banana-pro-preview)
- Curl-fallback in klantpagina stap 5A: als Python script faalt (httpx SOCKS proxy in Cowork), valt de skill terug op directe curl naar Gemini API + catbox.moe upload
- Interactieve AI-Readiness Quickscan: quiz draait nu als klikbare GitHub Pages app (JSON + base64 in URL), direct gelinkt op de klantpagina
- `ai-quiz` skill: standalone skill die quizvragen genereert als JSON, base64-encodeert en een klikbare quiz-URL bouwt
- Consultantfoto's geupload en team Excel bijgewerkt met foto-URL's
- Interactieve API key setup in Cowork: skill vraagt om GEMINI_API_KEY wanneer deze ontbreekt en slaat op als .env
- README met duidelijke configuratie-instructies (settings.json als primaire methode, .env als fallback)

### Changed
- Quiz-flow vereenvoudigd: stappen 6B/6C/6D (Notion sub-pagina, database, pre-fill) vervangen door een enkele interactieve quiz-URL op de klantpagina zelf
- Klantpagina paginastructuur herschreven: van 10 naar 9 secties, toekomstvisie als wow-moment na bedrijfsinfo
- Losse `AI-toekomstvisie.zip` verwijderd (content geintegreerd in klantpagina-skill)
- `gemini-image` skill herschreven met twee flows: lokaal (curl) en Cowork (browser MCP via Chrome)
- Klantpagina stap 5A herschreven met omgevingsdetectie en browser MCP flow voor Cowork
- Gemini model geupdate naar `gemini-3-pro-image-preview` in alle skills
- `build.sh` synct nu ook `gemini-image` skill naar plugin/
- Projectstructuur geherorganiseerd: scripts naar `scripts/`, teamdata naar `data/`, referentiemateriaal naar `docs/`
- Plugin-bestand hernoemd van `.plugin` naar `.zip`
- Skill herschreven met nieuwe UX-flow (parallelle stappen, bevestigingsscherm)
- PLAN.md, README.md en CLAUDE.md bijgewerkt naar huidige staat
- Env loading vereenvoudigd: van 5 .env zoekpaden naar 1-2 (projectroot + working dir)

### Removed
- Quiz sub-pagina, Notion database en pre-fill rij (stappen 6B/6C/6D) uit klantpagina-skill: vervangen door interactieve quiz-URL
- Secties "De AI Panda Aanpak (3 pijlers)", "7-Sterren AI-Maturity Model" en "Handige Links & Kennisbronnen" uit klantpagina template (generiek, lage wowfactor, vervangen door persoonlijke toekomstvisie)
- Generieke quote ("Wij bouwen aan 7-sterren organisaties") vervangen door persoonlijke pull quote uit toekomstvisie
- `AI-toekomstvisie.zip` skill (geintegreerd in klantpagina-skill)
- `load-env.sh` SessionStart hook verwijderd (werkte niet in Cowork vanwege bug #11649)

### Fixed
- Image generation in Cowork opgelost via curl-fallback (Python httpx faalde door SOCKS proxy restricties)
- GEMINI_API_KEY niet beschikbaar in Cowork opgelost via interactieve setup en settings.json documentatie

## [0.1.0] - 2026-02-17

Eerste werkende MVP: end-to-end flow van bedrijfsnaam tot Notion-klantpagina.

### Added
- Klantpagina skill met volledige wizard-workflow (7 stappen)
- Nano Banana Pro: AI-beeldgeneratie via Google Gemini met `--client` mode
- Logo-zoekpipeline: Google Favicons, website scrape, DuckDuckGo, image search
- AI-native logo-integratie via Gemini referentie-images
- Legacy badge-detectie en compositing via OpenCV (optioneel)
- Panda character referentiebeeld voor consistente generatie
- Sector-specifieke achtergronden (telecom, retail, zorg, logistiek, etc.)
- Gemini MCP server voor beeldgeneratie vanuit de plugin
- Prompt Optimizer met templates voor cartoon, foto, logo en artistiek
- Plugin packaging via `build.sh` (assembleert bronbestanden tot .zip)
- Plugin componenten: slash command, kwaliteitscheck hook, MCP server config
- Team-integratie: 13 consultants inlezen uit Excel
- Notion MCP koppeling: pagina's aanmaken met parent parameter
- Fallback-systeem voor alle externe calls (WebFetch, Gemini, Excel, Notion)
- Cloudinary upload als optionele persistent hosting
- catbox.moe upload als standaard tijdelijke hosting
- Projectdocumentatie: CLAUDE.md, PLAN.md, BACKLOG.md, README.md

### Fixed
- Badge-detectie y-range verbreed voor edge cases
- Notion parent parameter restrictie verwijderd
- Gemini model bijgewerkt naar gemini-3-pro-image-preview
