# Changelog

Alle noemenswaardige wijzigingen aan dit project worden hier gedocumenteerd.

Format gebaseerd op [Keep a Changelog](https://keepachangelog.com/nl/1.1.0/).
Dit project volgt [Semantic Versioning](https://semver.org/lang/nl/).

## [Unreleased]

*Geen wijzigingen.*

## [2.3.0] - 2026-02-19

Visuele verrijking en robuustheid: panda-karakter in elke Gamma-slide, merkkleuren doorheen de hele flow, landscape hero-afbeelding, Gemini-model vastgezet en Gamma image-model gecorrigeerd.

### Added
- **Terugkerend panda-karakter**: ai-toekomstvisie-v2 stuurt per slide een [Scene: ...] hint zodat de panda op minstens 7 van de 10 slides verschijnt
- **Merkkleur-extractie vroeg in de flow**: klantpagina-v2 stap 2A haalt nu MERKKLEUR_PRIMAIR, MERKKLEUR_SECUNDAIR en HUISSTIJL_KENMERK op via WebSearch/WebFetch; beschikbaar voor de hele flow

### Changed
- **Hero-afbeelding landscape**: panda-server.py genereert nu 16:9 afbeeldingen (Gemini `aspectRatio: 16:9`, OpenAI `1792x1024`)
- **Gemini model vastgezet**: gemini-image-v2/SKILL.md bevat nu een expliciete verbodsbepaling — model altijd `gemini-3-pro-image-preview`, nooit opzoeken of wisselen
- **Gamma image-model gecorrigeerd**: `flux-kontext-max` (PRO-only) vervangen door `flux-2-pro` (beschikbaar op standaardplan)
- **Gamma timeout-gedrag**: timeout wordt niet meer als fout behandeld; skill stopt en verwijst naar gamma.app/recent — geen dubbele presentaties
- **V1 skills gearchiveerd**: verplaatst naar `.claude/skills/_archive/`, niet meer meegebundeld in de plugin
- **AI Panda beschrijving uitgebreid**: template `klantpagina.md` bevat nu langere beschrijving met zin over samenwerking met teams op de werkvloer
- Plugin manifest versie: 2.2.0 → 2.3.0

## [2.2.0] - 2026-02-19

Foolproof Gamma-presentaties: dynamische thema-validatie, bedrijfslogo in headerFooter, merkkleur-integratie en robuuste 4-staps fallback-keten. LESSONS-LEARNED verplaatst naar projectroot.

### Added
- **Gamma thema-validatie**: `get_themes` wordt aangeroepen vóór `generate`; zoekt op "panda"/"AI Panda" dan "canaveral", anders geen themeId
- **Bedrijfslogo in Gamma**: `cardOptions.headerFooter.topRight` met bedrijfslogo via Logo.dev, alleen als WEBSITE_DOMEIN beschikbaar
- **Merkkleur in Gamma**: primaire merkkleur meegeven als design note in `inputText` (slide 1) én als stijl-hint in `imageOptions.style`
- **4-staps fallback-keten** bij Gamma-fouten: (1) volledig → (2) zonder cardOptions → (3) minimaal → (4) Markdown-fallback; elke poging logt wat is weggelaten
- **Post-generatie URL-validatie**: controleert na elke Gamma-call of response een `https://`-URL bevat vóór acceptatie
- **Conditionele stap 1A**: huisstijl-research overgeslagen als WEBSITE_DOMEIN + MERKKLEUR_PRIMAIR al meegegeven zijn
- **WEBSITE_DOMEIN afleiden**: bij stap 1A zonder input leid WEBSITE_DOMEIN af uit WebSearch-resultaten als fallback
- `LESSONS-LEARNED.md` verplaatst van `docs/` naar projectroot

### Changed
- **ai-toekomstvisie-v2 aanroep-interface**: accepteert nu ook `WEBSITE_DOMEIN` en `MERKKLEUR_PRIMAIR` als optionele inputparameters
- **klantpagina-v2 stap 8**: geeft WEBSITE_DOMEIN + MERKKLEUR_PRIMAIR door aan ai-toekomstvisie-v2 (bespaart extra WebSearch-ronde)
- **Fallback-beschrijving**: hardcoded themeId `0r1msp6zfjh4o59` vervangen door dynamische lookup
- Plugin manifest versie: 2.1.0 → 2.2.0

## [2.1.0] - 2026-02-19

OpenAI fallback, fotorealistische panda-prompt, bedrijfslogo-integratie, en robuustere externe services.

### Added
- **OpenAI fallback**: `gpt-image-1.5` als fallback wanneer Gemini faalt (rate limits). Automatische fallback-keten: Gemini (met referentie-image) → OpenAI (prompt-only)
- **Panda referentie-image**: `panda-reference.png` wordt bij startup als base64 geladen en multimodal meegegeven aan Gemini voor stijlconsistentie
- **Bedrijfslogo-integratie**: Logo ophalen via Logo.dev (primair) of Google Favicons (fallback), meegeven als extra `inlineData` aan Gemini. Logo verschijnt op schermen, badges en whiteboards in de afbeelding
- **`generate_with_openai()` functie**: POST naar OpenAI images/generations endpoint, model `gpt-image-1.5`, `1024x1024`, quality `high`
- **`_fetch_logo_b64()` functie**: Haalt bedrijfslogo op als base64 via curl (SSL-robuust)
- **`upload_to_tmpfiles()` functie**: Upload naar tmpfiles.org met automatische `/dl/` directe-link conversie
- **`check_api_keys` MCP tool**: Retourneert `{"gemini": true/false, "openai": true/false}`
- **`set_api_key` MCP tool**: Accepteert `provider` ("gemini" of "openai") + `api_key`
- `OPENAI_API_KEY` en `LOGO_DEV_TOKEN` in `.mcp.json` env-sectie
- `sector` en `website` parameters op `generate_panda_image` tool

### Changed
- **Panda-prompt herschreven**: van cartoon ("cute friendly cartoon panda with t-shirt") naar fotorealistisch ("photorealistic giant panda in black business suit, orange necktie, furry paws, cinematic photography")
- **Logo API**: Clearbit (sunset dec 2025) vervangen door Logo.dev + Google Favicons fallback
- **Upload primair**: catbox.moe (was 0x0.st, nu 403). tmpfiles.org als fallback
- **Logo fetching**: `urllib.request` vervangen door `subprocess` + `curl` (voorkomt Python SSL-certificaatproblemen)
- **gemini-image-v2 skill**: stap 2 checkt nu beide API keys, fallback-keten bevat OpenAI, curl-fallbacks gebruiken catbox/tmpfiles
- **klantpagina-v2 skill**: API key check gebruikt `check_api_keys`, stap 5A gebruikt `generate_panda_image` MCP tool met `sector` + `website` parameters
- Plugin manifest versie: 2.0.0 → 2.1.0

### Removed
- `check_gemini_api_key` MCP tool (vervangen door `check_api_keys`)
- `set_gemini_api_key` MCP tool (vervangen door `set_api_key`)
- `upload_to_0x0()` functie (0x0.st retourneert 403)
- Clearbit Logo API referenties

## [2.0.0] - 2026-02-19

Volledige herbouw van de plugin met orchestrator-architectuur. Alle 4 skills herschreven als v2 met quick mode, MCP server uitgebreid, template geëxtraheerd, hooks verwijderd.

### Added
- **klantpagina-v2 skill**: orchestrator (~220 regels, was 678) die delegeert naar sub-skills via quick mode
- **gemini-image-v2 skill**: quick mode interface, fallback_url logica bij MCP response, opgeschoonde diagnostics
- **ai-quiz-v2 skill**: quick mode interface, optionele Notion-pagina (alleen standalone), Python-first base64 encoding
- **ai-toekomstvisie-v2 skill**: quick mode interface, kwaliteitscheck inline verplaatst naar stap 3 (pre-validatie)
- `read_team_excel` MCP tool: leest team Excel via CLAUDE_PLUGIN_ROOT met find-fallback, retourneert JSON
- `check_gemini_api_key` MCP tool: controleert of API key beschikbaar is in de sessie
- `set_gemini_api_key` MCP tool: slaat API key op in geheugen (nooit op schijf, verdwijnt bij sessie-einde)
- `plugin/templates/klantpagina.md`: Notion syntax referentie + volledig template met placeholders
- Gamma MCP tools toegevoegd aan /klantpagina command allowed-tools

### Changed
- MCP server hernoemd: `gemini-image-server.py` → `panda-server.py`
- MCP server naam: `gemini-images` → `panda-server`
- `/klantpagina` command verwijst nu naar klantpagina-v2 skill
- `build.sh` synct v2 skills, bundelt templates, verwijdert oude bestanden
- Plugin manifest versie: 0.2.0 → 2.0.0
- API key management: van bash `export` (shell-only) naar MCP tool (server + shell)

### Removed
- `plugin/hooks/hooks.json` en hooks directory (quality check niet meer nodig, sub-skills melden eigen status)
- `plugin/servers/gemini-image-server.py` (vervangen door panda-server.py)
- Inline Excel-leeslogica uit klantpagina (50 regels → MCP tool)
- Inline image-generatie uit klantpagina (175 regels → delegatie naar gemini-image-v2)
- Inline quiz-generatie uit klantpagina (65 regels → delegatie naar ai-quiz-v2)
- Inline Notion template uit klantpagina (140 regels → apart bestand)
- Omgevingsdetectie bash uit klantpagina (sub-skills handelen dit zelf af)
- `[DIAG]` diagnostics uit klantpagina (sub-skills melden zelf hun status)
- Health check stap 0 uit klantpagina flow

## [0.3.0] - 2026-02-19

Notion markdown syntax gefixed, Cowork image pipeline robuust gemaakt, lessons learned gedocumenteerd.

### Fixed
- Notion callouts: `<callout>` HTML-tags vervangen door Pandoc-style fenced divs (`::: callout {icon="emoji"}`)
- Notion kolommen: children tab-inspringing toegevoegd (zonder tabs werden kolommen leeg gerenderd)
- Notion teamfoto's: image captions verwijderd (`![](url)` i.p.v. `![[naam]](url)`) zodat er geen grijze tekst onder foto's verschijnt
- Notion embed: niet-bestaande `<embed>` tag verwijderd, vervangen door gewone link
- Gemini model: `gemini-2.0-flash-exp` (404) overal vervangen door `gemini-3-pro-image-preview`
- MCP server: `httpcore[socks]` toegevoegd aan bootstrap voor SOCKS proxy in Cowork
- catbox.moe 504 timeouts: teamfoto's opnieuw gehost op 0x0.st als fallback

### Added
- `upload_image_base64` MCP tool: server-side image upload naar catbox.moe (omzeilt CORS in Cowork)
- Inline Notion markdown syntax-referentie in klantpagina skill (met expliciete FOUT-voorbeelden)
- `docs/LESSONS-LEARNED.md`: gedocumenteerde lessen uit Cowork en Notion debugging
- `assets/nophoto.png`: placeholder avatar voor consultants zonder foto
- `DEMO-CHECKLIST.md`: 10-stappen dry-run procedure voor Cowork demo's

### Changed
- Skill template volledig herschreven met correcte Notion markdown syntax
- Plugin zip opnieuw gebouwd met alle fixes

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
