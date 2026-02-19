# Demo Checklist - AI Panda Klantpagina in Claude Cowork

Stapsgewijze dry-run procedure voor de demonstratie. Loop deze checklist door voordat je live gaat.

**Testbedrijf:** Gebruik een echt bedrijf (bijv. Coolblue, Picnic, Bol) zodat WebSearch realistische resultaten geeft.

---

## Pre-flight (voor de demo)

### 1. Plugin installatie
- [ ] Open Claude Cowork (nieuwste versie)
- [ ] Installeer `ai-panda-klantpagina.zip` via Instellingen > Plugins
- [ ] Controleer dat de plugin geladen is: skills, commands en MCP server zichtbaar
- [ ] Controleer dat `/klantpagina` als slash command beschikbaar is

### 2. GEMINI_API_KEY
- [ ] Verifieer dat de key in `~/.claude/settings.json` staat:
```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+OK (${#GEMINI_API_KEY} chars)}"
```
- [ ] Als "OK" niet verschijnt: voeg de key toe aan `~/.claude/settings.json` onder `"env"`
- [ ] Herstart Cowork na het toevoegen van de key

### 3. Notion MCP
- [ ] Controleer dat de Notion MCP server verbonden is (zichtbaar in Cowork MCP-status)
- [ ] Test met een simpele Notion-query (bijv. `notion-search` met een bekende pagina)

### 4. Excel teambestand
- [ ] Controleer dat `ai-panda-team.xlsx` in de plugin zit:
```bash
echo "CLAUDE_PLUGIN_ROOT: $CLAUDE_PLUGIN_ROOT"
ls "$CLAUDE_PLUGIN_ROOT/data/ai-panda-team.xlsx" 2>/dev/null && echo "OK" || echo "NIET GEVONDEN"
```
- [ ] Als CLAUDE_PLUGIN_ROOT leeg is: controleer of `find` het bestand vindt

---

## Smoke test (snelle doorloop)

### 5. WebSearch
- [ ] Voer handmatig een WebSearch uit op het testbedrijf
- [ ] Resultaat bevat bedrijfsnaam, sector en omschrijving

### 6. Afbeelding generatie (MCP server)
- [ ] Test `generate_panda_image` MCP tool met testbedrijf
- [ ] Resultaat bevat `"success": true` en een werkende `image_url`
- [ ] Open de URL in een browser: afbeelding is zichtbaar

### 7. Afbeelding upload (fallback)
- [ ] Test `upload_image_base64` MCP tool met een kleine test-string:
```
MCP tool: upload_image_base64
  image_base64: "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
  filename: "test.png"
```
- [ ] Resultaat bevat `"success": true` en een werkende URL

### 8. Quiz URL
- [ ] Genereer een test quiz-URL (of gebruik een eerdere)
- [ ] Open de URL in de browser: quiz laadt correct met vragen
- [ ] URL lengte is < 2000 tekens (controleer in adresbalk)

---

## End-to-end test

### 9. Volledige /klantpagina flow
- [ ] Typ `/klantpagina` en doorloop alle stappen met het testbedrijf
- [ ] Stap 2A: bedrijfsinfo wordt opgehaald (WebSearch)
- [ ] Stap 2B: teamleden worden geladen uit Excel
- [ ] Stap 3: consultants selecteerbaar via multiSelect
- [ ] Stap 4: bevestigingsscherm toont correcte info
- [ ] Stap 5A: panda-afbeelding gegenereerd met publieke URL (geen placeholder)
- [ ] Stap 5D: toekomstverhaal geschreven
- [ ] Stap 5E: visie-afbeelding gegenereerd met publieke URL
- [ ] Stap 6: Notion-pagina aangemaakt

### 10. Notion-pagina controleren
- [ ] Open de Notion-URL
- [ ] Hero-afbeelding zichtbaar (niet placeholder)
- [ ] Bedrijfsinfo correct
- [ ] Toekomstverhaal aanwezig met pull quote
- [ ] Visie-afbeelding zichtbaar
- [ ] Teamleden met foto's
- [ ] Roadmap met sector-specifieke content
- [ ] Quiz-link werkend (klikbaar, quiz laadt)
- [ ] Quiz embed werkend (als Notion dit ondersteunt voor GitHub Pages)

---

## Bekende aandachtspunten

| Onderdeel | Risico | Fallback |
|---|---|---|
| MCP generate_panda_image | Kan falen door proxy/netwerk | Browser JS + upload_image_base64 |
| Catbox.moe upload | CORS in browser, timeout | upload_image_base64 MCP tool (server-side) |
| Notion embed quiz | GitHub Pages mogelijk niet in whitelist | Tekstlink als fallback (staat al in template) |
| Excel niet gevonden | CLAUDE_PLUGIN_ROOT leeg | find-commando, daarna handmatige invoer |
| GEMINI_API_KEY ontbreekt | Niet in settings.json | Interactieve vraag in stap 5A |
| WebSearch geen resultaten | Bedrijf te klein/onbekend | Gebruiker vult handmatig in |

---

## Na de demo

- [ ] Testpagina opruimen in Notion (of bewaren als voorbeeld)
- [ ] Eventuele issues noteren voor verbetering
