# Changelog

Alle noemenswaardige wijzigingen aan dit project worden hier gedocumenteerd.

Format gebaseerd op [Keep a Changelog](https://keepachangelog.com/nl/1.1.0/).
Dit project volgt [Semantic Versioning](https://semver.org/lang/nl/).

## [Unreleased]

### Added
- Interactieve API key setup in Cowork: skill vraagt om GEMINI_API_KEY wanneer deze ontbreekt en slaat op als .env
- README met duidelijke configuratie-instructies (settings.json als primaire methode, .env als fallback)

### Changed
- Projectstructuur geherorganiseerd: scripts naar `scripts/`, teamdata naar `data/`, referentiemateriaal naar `docs/`
- Plugin-bestand hernoemd van `.plugin` naar `.zip`
- Skill herschreven met nieuwe UX-flow (parallelle stappen, bevestigingsscherm)
- PLAN.md, README.md en CLAUDE.md bijgewerkt naar huidige staat
- Env loading vereenvoudigd: van 5 .env zoekpaden naar 1-2 (projectroot + working dir)

### Removed
- `load-env.sh` SessionStart hook verwijderd (werkte niet in Cowork vanwege bug #11649)

### Fixed
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
