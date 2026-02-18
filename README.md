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

- **AI-gegenereerde afbeelding** in de AI Panda-stijl, met het bedrijfslogo verwerkt via Gemini
- **Bedrijfsprofiel** met omschrijving, automatisch opgehaald van de website
- **Consultantteam** met foto, functie en contactgegevens
- **AI Implementatie Roadmap** in vier fases, specifiek voor de sector van de klant
- **Volgende stappen** als checklist om direct mee te starten

---

## Aan de slag

### 1. Plugin installeren

Download `ai-panda-klantpagina.zip` uit deze repository en installeer het in Claude Cowork:

1. Open **Claude Cowork**
2. Ga naar **Instellingen** > **Plugins**
3. Klik op **Plugin toevoegen** en selecteer het `.zip` bestand

### 2. API-key instellen

De plugin gebruikt Google Gemini voor beeldgeneratie. Je hebt een (gratis) API-key nodig:

| Key | Waarvoor | Aanmaken |
|---|---|---|
| `GEMINI_API_KEY` | AI-beeldgeneratie | [Google AI Studio](https://aistudio.google.com/apikey) |

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

plugin/                   Plugin bronbestanden (wordt gezipt door build.sh)
  commands/klantpagina.md     /klantpagina slash command
  servers/gemini-image-server.py  MCP server voor Gemini
  hooks/hooks.json            Automatische kwaliteitscheck
  skills/klantpagina/SKILL.md     Volledige skill-workflow

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
| **Klantpagina Skill** | De volledige wizard: van bedrijfsnaam naar Notion-pagina |
| **Gemini MCP Server** | Beeldgeneratie via Google Gemini, upload naar catbox.moe |
| **Nano Banana Pro** | Geavanceerd Python-script met logo-zoekpipeline en sector-specifieke achtergronden |
| **Prompt Optimizer** | Maakt van een simpele beschrijving een professionele Gemini-prompt |
| **Kwaliteitscheck Hook** | Controleert automatisch of de gegenereerde pagina compleet en specifiek is |

---

## Status

Fase 1 (MVP) is afgerond. De end-to-end flow werkt: van bedrijfsnaam tot Notion-pagina.

Momenteel in ontwikkeling: Notion-template met strakke huisstijl, AI-quiz (Noud), toekomstvisie (Rick).

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

Intern project van **AI Panda** voor het automatiseren van klantprocessen.
