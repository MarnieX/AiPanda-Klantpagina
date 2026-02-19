# Backlog

**Deadline tussenstand:** Donderdag 20 februari (einde dag)

## Fase 1: MVP (technisch werkend)
- [x] ✅ Minimale plugin opzetten met basis skill-structuur — `plugin/` bronmap + `build.sh` (Marnix)
- [x] ✅ Notion MCP koppeling testen: pagina aanmaken vanuit skill — werkt, incl. parent parameter (Marnix)
- [x] ✅ Nano Banana Pro integratie testen: panda-afbeelding genereren via Gemini — werkt met `--client` mode (Marnix)
- [x] ✅ Team-integratie testen: consultants uit Excel inlezen — 13 teamleden geladen (Marnix)
- [x] ✅ End-to-end flow testen: van klantnaam tot Notion-pagina — bol.com klantpagina aangemaakt (Marnix)

## Fase 2: Features uitbouwen
- [x] ✅ Notion-pagina template bouwen met strakke opmaak en AI Panda huisstijl — hero banner, 3 pijlers, teamtabel, roadmap met quotes, 7-sterren model, kennislinks (Marnix)
- [x] ✅ Klantpagina skill volledig uitwerken met alle stappen — skill bijgewerkt met logo compositing, lokale paden, --client mode (Marnix)
- [x] ✅ AI-quiz geintegreerd in klantpagina flow: 5 sector-specifieke vragen, interactieve GitHub Pages quiz-URL direct op de klantpagina (Marnix)
- [x] ✅ Interactieve quiz vervangt Notion database: JSON + base64 in URL, geen sub-pagina/database meer nodig (Marnix)
- [x] ✅ Standalone `ai-quiz` skill: genereert quiz JSON, bouwt klikbare URL, optioneel Notion-pagina (Marnix)
- [x] ✅ Toekomstvisie geintegreerd in klantpagina-skill: pull quote, 10-jaar verhaal, gebrandde visie-afbeelding, kerngetallen. Losse AI-toekomstvisie.zip verwijderd (Marnix)
- [ ] 🟡 Prompt Optimizer valideren en finetunen (Marnix)
- [x] ✅ Fallback-systeem implementeren voor elke externe call — fallbacks gedocumenteerd in skill voor alle stappen (Marnix)
- [x] ✅ Generieke `gemini-image` skill: standalone image generation via curl en Nano Banana Pro, werkt in Cowork (Marnix)
- [x] ✅ Curl-fallback voor image generation in klantpagina: omzeilt httpx SOCKS proxy probleem in Cowork (Marnix)
- [x] ✅ Browser MCP flow voor image generation: omgevingsdetectie (local/Cowork), Chrome MCP-bridge voor Gemini API calls wanneer sandbox curl blokkeert (Marnix)
- [x] ✅ Consultantfoto's geupload en team Excel bijgewerkt met URL's (Marnix)

## Fase 2.5: v2.0 verbeteringen
- [x] ✅ Plugin v2.0.0: orchestrator-architectuur met sub-skills, MCP server uitgebreid, template geëxtraheerd, hooks verwijderd (Marnix)
- [x] ✅ Session-safe API key management via MCP tools (check/set, in-memory only) (Marnix)
- [ ] 🔴 Gemini image generation faalt bij hoge load (rate limit / overbelast). Fallback toevoegen naar OpenAI image model (gpt-image-1 of nieuwste beschikbaar). panda-server.py uitbreiden met OPENAI_API_KEY + OpenAI als secondary image provider na Gemini failure (Marnix)

## Fase 3: Polish & distributie
- [x] ✅ Plugin ombouwen en packaging voor Cowork — `build.sh` assembleert .plugin bestand vanuit bronmap (Marnix)
- [x] ✅ GEMINI_API_KEY loading waterdicht gemaakt — settings.json als primaire methode, interactieve setup in Cowork, obsolete load-env.sh hook verwijderd (Marnix)
- [x] ✅ README bijgewerkt met settings.json configuratie-instructies (Marnix)
- [ ] 🟡 Plugin installatie testen in Cowork met browser MCP image generation flow (Marnix)
- [ ] 🟡 Verhaal rondom Claude Cowork uitwerken voor de demonstratie (Rick)
- [ ] 🟡 Onboarding documentatie voor medestudenten: installatie, setup, hoe bij te dragen (Marnix)
- [ ] 🟡 Branch protection instellen op main: PR-reviews verplicht (Marnix)
