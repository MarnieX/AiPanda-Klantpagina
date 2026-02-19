# 🐼 AI Panda Klantpagina Generator

> Van bedrijfsnaam naar professionele Notion-klantpagina — volledig automatisch.

Een **Claude Cowork plugin** waarmee AI Panda consultants in een paar minuten een complete, gepersonaliseerde klantpagina genereren. Bedrijfsinfo, merkkleuren, AI-roadmap, quiz, panda-afbeelding en een toekomstvisie-presentatie: alles wordt automatisch samengesteld en direct in Notion klaargezet.

---

## ✨ Wat krijg je

Eén `/klantpagina` commando levert een volledige Notion-pagina op:

| Onderdeel | Wat het doet |
|-----------|-------------|
| 🖼️ **Hero-afbeelding** | Fotorealistische panda in de herkenbare AI Panda stijl, gegenereerd door Gemini met bedrijfslogo |
| 💬 **2028-quote** | Pakkende uitspraak van een fictieve medewerker over hoe hun werk er in 2028 uitziet |
| 🏢 **Bedrijfsprofiel** | Twee kolommen: Over het bedrijf + Over AI Panda, gevuld met echte bedrijfsinfo |
| 👥 **Consultantteam** | Foto, naam, functie en contact van alle betrokken AI Panda consultants |
| 🗺️ **AI Roadmap** | Sector-specifieke implementatiefases, op maat gemaakt voor de klant |
| 🧠 **AI-Readiness Quiz** | Interactieve 5-vragen quiz direct als embed op de pagina |
| 🎯 **Toekomstvisie** | Gamma.app presentatie van 10 slides met het 10-jaar AI-transformatieverhaal |

---

## 🚀 Hoe het werkt

Typ `/klantpagina` in Claude Cowork en doorloop de wizard:

```
1. 🏷️  Bedrijfsnaam of URL opgeven
2. 🔍  Bedrijfsinfo + merkkleuren worden automatisch opgehaald
3. 👤  Consultants kiezen uit het teambestand
4. ✅  Samenvatting bevestigen
5. ⚡  Alles wordt parallel gegenereerd:
        → AI Panda hero-afbeelding (Gemini + logo)
        → Sector-specifieke AI roadmap
        → Interactieve quiz-URL
        → 2028-medewerker quote
6. 📄  Notion-pagina wordt aangemaakt
7. 🔗  Je krijgt direct de Notion-URL + Quiz-URL
8. 🎬  Gamma-presentatie wordt aangemaakt (op de achtergrond)
```

Totale doorlooptijd: **3-5 minuten** van bedrijfsnaam tot complete klantpagina.

---

## 🏗️ Technische architectuur

```
Claude Cowork
    │
    ▼
/klantpagina command
    │
    ▼
klantpagina-v2 skill (orchestrator)
    ├── WebSearch + WebFetch ──── bedrijfsinfo + merkkleuren
    ├── panda-server MCP ──────── read_team_excel, generate_panda_image
    ├── Notion MCP ────────────── pagina aanmaken
    └── Sub-skills (parallel):
            ├── gemini-image-v2 ─ AI Panda hero-afbeelding
            ├── ai-quiz-v2 ────── interactieve Readiness Quiz
            └── ai-toekomstvisie-v2 ── Gamma presentatie
```

### Panda-afbeelding fallback-keten
```
Gemini (multimodal: panda-referentie + bedrijfslogo)
  → OpenAI gpt-image-1.5 (prompt-only)
    → Placeholder (flow stopt nooit)
```

### Gamma presentatie fallback-keten
```
Poging 1: flux-2-pro + themeId + logo in header + merkkleuren
  → Poging 2: zonder logo (cardOptions weggelaten)
    → Poging 3: minimale parameters
      → Poging 4: Markdown-outline in chat
```

> **Timeout-proof:** Een Gamma-timeout ≠ fout. Het request is al verzonden. De skill stopt bij een timeout en verwijst naar gamma.app/recent — geen dubbele presentaties.

---

## 🧩 Skills

### 🎯 `klantpagina-v2` — De orchestrator
De hoofdskill. Coördineert alle sub-skills, leest het teambestand, haalt bedrijfsinfo op, en bouwt de Notion-pagina vanuit een template. Paralleliseert zoveel mogelijk om snelheid te winnen.

**Input:** bedrijfsnaam of URL
**Output:** Notion-klantpagina URL + Quiz-URL + Gamma-presentatie URL

---

### 🖼️ `gemini-image-v2` — AI-beeldgeneratie
Genereert fotorealistische panda-afbeeldingen via Gemini (primair) of OpenAI (fallback). Werkt standalone én vanuit andere skills via quick mode. Gebruikt `panda-reference.png` als multimodal referentie voor stijlconsistentie.

**Input:** Engelse prompt
**Output:** publieke afbeeldings-URL

---

### 🧠 `ai-quiz-v2` — Interactieve Readiness Quiz
Genereert 5 sector-specifieke quizvragen als JSON, base64-encodeert ze en bouwt een klikbare URL naar de GitHub Pages quiz-app. Geen server nodig — alles zit in de URL.

**Input:** bedrijfsnaam, sector
**Output:** quiz-URL (direct klikbaar, embed-ready voor Notion)

---

### 🎬 `ai-toekomstvisie-v2` — Gamma Presentatie
Schrijft een visionair 10-jaar transformatieverhaal voor de klant en bouwt daar een professionele Gamma.app pitch-presentatie van 10 slides van. De panda verschijnt als terugkerend karakter op minstens 7 slides. Gebruikt merkkleuren en het bedrijfslogo automatisch.

**Input:** bedrijfsnaam, sector, omschrijving, merkkleuren (optioneel)
**Output:** Gamma presentatie-URL

---

## 🛠️ MCP Server — `panda-server`

De Python MCP server die de plugin aandrijft:

| Tool | Wat het doet |
|------|-------------|
| `generate_panda_image` | Gemini + OpenAI beeldgeneratie, logo ophalen, upload naar catbox/tmpfiles |
| `read_team_excel` | AI Panda team inlezen uit `ai-panda-team.xlsx` |
| `check_api_keys` | Controleert of Gemini + OpenAI keys beschikbaar zijn |
| `set_api_key` | Slaat een API key op in geheugen (sessie-scope, nooit op schijf) |
| `upload_image_base64` | Server-side upload van base64-afbeelding (omzeilt CORS in Cowork) |

---

## ⚙️ Setup

### 1. Plugin installeren

Download `ai-panda-klantpagina.zip` en installeer in Claude Cowork:

```
Cowork → Instellingen → Plugins → Plugin toevoegen → selecteer .zip
```

### 2. API keys instellen

Voeg toe aan `~/.claude/settings.json`:

```json
{
  "env": {
    "GEMINI_API_KEY": "AIza...",
    "OPENAI_API_KEY": "sk-..."
  }
}
```

| Key | Service | Nodig voor |
|-----|---------|-----------|
| `GEMINI_API_KEY` | Google Gemini | Hero-afbeelding (primair) |
| `OPENAI_API_KEY` | OpenAI | Hero-afbeelding (fallback) |

Zonder keys werkt de plugin gewoon door — met een placeholder-afbeelding.

### 3. Klantpagina genereren

```
/klantpagina
```

---

## 📁 Projectstructuur

```
.claude/skills/
  klantpagina-v2/         Orchestrator skill
  gemini-image-v2/        AI-beeldgeneratie skill
  ai-quiz-v2/             Quiz-generator skill
  ai-toekomstvisie-v2/    Gamma-presentatie skill
  _archive/               Gearchiveerde v1 skills (niet actief)

plugin/
  commands/klantpagina.md   /klantpagina slash command
  servers/panda-server.py   MCP server
  templates/klantpagina.md  Notion page template
  skills/                   Gesyncte skills voor distributie

assets/
  panda-reference.png       Panda referentiebeeld voor Gemini
  *.jpeg / *.png            Showcase-afbeeldingen (klantexempels)

data/
  ai-panda-team.xlsx        Teambestand met alle consultants

quiz/                       GitHub Pages quiz-app (submodule)
scripts/                    Lokale hulpscripts (generate, optimize)
build.sh                    Bouwt plugin/ naar ai-panda-klantpagina.zip
```

---

## 🧪 Readiness test

Snelle gate op de kritieke flow (afbeelding → Notion):

```bash
./scripts/cowork-readiness.sh
```

Rapporteert: `IMAGE_GENERATION` · `NOTION_IMAGE_EMBED` · `OVERALL`

---

## 📋 Status

**v2.2.0** — Productieklaar. End-to-end getest: van bedrijfsnaam tot Notion-klantpagina met hero-afbeelding, roadmap, quiz, 2028-quote en Gamma-toekomstvisie.

Zie [BACKLOG.md](./BACKLOG.md) voor openstaande taken en [CHANGELOG.md](./CHANGELOG.md) voor versiegeschiedenis.

---

Intern project van **AI Panda** · [aipanda.nl](https://aipanda.nl)
