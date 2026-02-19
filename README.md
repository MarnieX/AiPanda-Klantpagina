# AI Panda - Klantpagina Generator

> Van bedrijfsnaam naar professionele Notion-klantpagina, volledig automatisch.

De Klantpagina Generator is een **Claude Cowork plugin** waarmee consultants van AI Panda in een paar stappen een complete klantpagina aanmaken in Notion. Bedrijfsinfo wordt automatisch opgehaald, een AI-gegenereerde panda-afbeelding gemaakt, en het team gekoppeld. Geen templates invullen, geen handwerk.

---

## Hoe werkt het?

Je typt `/klantpagina` in Claude Cowork en volgt drie stappen:

1. **Bedrijfsnaam opgeven** - de plugin haalt automatisch bedrijfsinfo op van de website
2. **Consultants kiezen** - selecteer wie er aan dit project werkt (uit het teambestand)
3. **Bevestigen** - controleer de samenvatting en klik op akkoord

De rest gaat automatisch: afbeelding genereren, content samenstellen, Notion-pagina aanmaken. Je krijgt een klikbare link terug.

---

## Wat staat er op de klantpagina?

Elke gegenereerde pagina bevat:

- **AI-gegenereerde hero-afbeelding** in de AI Panda-stijl via Gemini
- **2028-quote**: pakkende uitspraak van een fictieve medewerker over hoe hun werk er in 2028 uitziet dankzij AI
- **Twee-koloms bedrijfsprofiel**: "Over [Bedrijf]" (omschrijving, sector, website) naast "Over AI Panda" (missie, tagline)
- **Consultantteam** met foto, functie, telefoonnummer en e-mail in kolommen
- **AI Implementatie Roadmap** in vier fases, specifiek voor de sector van de klant
- **AI-Readiness Quickscan**: interactieve quiz (5 sector-specifieke vragen) direct als embed op de pagina

---

## Aan de slag

### 1. Plugin installeren

Download `ai-panda-klantpagina.zip` uit deze repository en installeer het in Claude Cowork:

1. Open **Claude Cowork**
2. Ga naar **Instellingen** > **Plugins**
3. Klik op **Plugin toevoegen** en selecteer het `.zip` bestand

### 2. API-key instellen

De plugin gebruikt Google Gemini (primair) en optioneel OpenAI (fallback) voor beeldgeneratie:

| Key | Waarvoor | Aanmaken |
|---|---|---|
| `GEMINI_API_KEY` | AI-beeldgeneratie (primair) | [Google AI Studio](https://aistudio.google.com/apikey) |
| `OPENAI_API_KEY` | AI-beeldgeneratie (fallback) | [OpenAI Platform](https://platform.openai.com/api-keys) |

**Methode 1: Claude Code settings.json (aanbevolen)**

Dit is de meest betrouwbare methode en werkt in alle omgevingen (Cowork, CLI, hooks, Bash).

User-level (geldt voor alle projecten):
```json
// ~/.claude/settings.json
{
  "env": {
    "GEMINI_API_KEY": "jouw-key-hier"
  }
}
```

Of project-level (alleen dit project):
```json
// .claude/settings.local.json (staat in .gitignore)
{
  "env": {
    "GEMINI_API_KEY": "jouw-key-hier"
  }
}
```

**Methode 2: .env bestand (fallback)**

```bash
cp .env.example .env
# Vul je GEMINI_API_KEY in
```

> **Let op:** In Cowork (Claude Desktop) wordt het `.env` bestand niet automatisch geladen door de SessionStart hook vanwege een bekende beperking. Gebruik in dat geval methode 1.

Zonder API-key werkt de plugin nog steeds, maar met een placeholder-afbeelding.

### 3. Klantpagina genereren

Typ `/klantpagina` in Claude Cowork en volg de wizard.

---

## Projectstructuur

```
scripts/                  Python scripts voor beeldgeneratie
  generate_notion_image.py    Nano Banana Pro (Gemini image pipeline)
  prompt-optimizer.py         Prompt templates voor verschillende stijlen
  banana.sh                   CLI wrapper

plugin/                   Plugin bronbestanden
  commands/klantpagina.md     /klantpagina slash command
  servers/panda-server.py     MCP server (Gemini + OpenAI + logo + Excel)
  templates/klantpagina.md    Notion template
  skills/klantpagina-v2/SKILL.md  Orchestrator-workflow

assets/                   Referentiebestanden
  panda-reference.png         Panda character referentie voor Gemini

data/                     Projectdata
  ai-panda-team.xlsx          Teambestand met alle consultants

docs/                     Referentiemateriaal, vergaderverslagen, presentaties
```

---

## Onderdelen

| Onderdeel | Beschrijving |
|---|---|
| **Klantpagina Skill** | De volledige wizard: van bedrijfsnaam naar Notion-pagina met toekomstvisie en quiz |
| **AI-Quiz Skill** | Standalone skill: genereert interactieve AI-Readiness quiz als klikbare URL |
| **Gemini Image Skill** | Standalone image generation via curl (lokaal) of browser MCP (Cowork) |
| **Panda MCP Server** | Beeldgeneratie via Gemini/OpenAI, logo-resolutie, Excel parsing, upload via catbox/tmpfiles |
| **Nano Banana Pro** | Python-script met logo-zoekpipeline en sector-specifieke achtergronden |
| **Prompt Optimizer** | Maakt van een simpele beschrijving een professionele Gemini-prompt |

---

## Status

Fase 1 (MVP), Fase 2 (Features) en Fase 3 (Component Review) zijn afgerond. v2.2 draait end-to-end: van bedrijfsnaam tot Notion-klantpagina met 2028-quote, roadmap, quiz en Gamma-toekomstvisie.

Openstaand: prompt optimizer finetunen, onboarding documentatie, plugin-installatie validatie in Cowork.

Zie [BACKLOG.md](./BACKLOG.md) voor het volledige takenoverzicht.

---

## Documentatie

| Bestand | Inhoud |
|---|---|
| [PLAN.md](./PLAN.md) | Architectuur, features en technische details |
| [BACKLOG.md](./BACKLOG.md) | Openstaande taken per fase |
| [CHANGELOG.md](./CHANGELOG.md) | Versiegeschiedenis |
| [CLAUDE.md](./CLAUDE.md) | AI-agent instructies voor dit project |

---

## Cowork Readiness Test (zonder Cowork)

Voor een snelle gate op de kritieke flow "afbeelding genereren -> in Notion-content opnemen":

```bash
./scripts/cowork-readiness.sh
```

Dit script draait Cowork-simulatie-tests en rapporteert:
- `IMAGE_GENERATION`
- `NOTION_IMAGE_EMBED`
- `OVERALL`

---

Intern project van **AI Panda** voor het automatiseren van klantprocessen.
