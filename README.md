# 🐼 AI Panda - Klantpagina Generator

> Van klantnaam naar complete Notion-pagina in een paar seconden.

Met de Klantpagina Generator maken consultants van **AI Panda** razendsnel professionele klantpagina's aan in Notion. Geen handmatig kopieerwerk, geen losse templates. Geef een bedrijfsnaam op en de rest gebeurt automatisch.

---

## 🎯 Wat doet het?

**Het probleem:** Voor elke nieuwe klant maak je handmatig een Notion-pagina aan. Bedrijfsinfo opzoeken, afbeelding zoeken of maken, template invullen, roadmap aanmaken. Dat kost tijd en ziet er niet altijd consistent uit.

**De oplossing:** Deze plugin automatiseert het hele proces. Je typt `/klantpagina`, geeft een bedrijfsnaam op, en binnen een paar seconden staat er een complete, professionele klantpagina in Notion.

---

## 📄 Wat staat er op de klantpagina?

Elke gegenereerde klantpagina bevat:

- 🖼️ **AI-gegenereerde afbeelding** in de herkenbare AI Panda-stijl, met de bedrijfsnaam op het shirt van de panda-mascotte
- 🏢 **Bedrijfsprofiel** met een korte omschrijving, automatisch opgehaald van de website van de klant
- 👥 **Consultantteam** met foto, functie en contactgegevens van de gekoppelde AI Panda-consultants
- 🗺️ **AI Implementatie Roadmap** in vier fases (Discovery, Pilot, Implementatie, Schaling), specifiek toegespitst op de sector van de klant
- ✅ **Volgende stappen** als checklist om direct mee aan de slag te gaan

Het resultaat: een consistente, professionele uitstraling voor elke klant, zonder handwerk.

---

## ⚡ Hoe werkt het?

### Via Claude Code (aanbevolen)

Typ simpelweg `/klantpagina` in Claude Code en volg de stappen. Claude vraagt om de klantnaam, haalt alles op en maakt de pagina aan.

### De afbeeldingen-tool los gebruiken

Wil je alleen een afbeelding genereren (bijvoorbeeld voor een presentatie of social post)? Dat kan ook los:

```
./banana.sh "een panda die code schrijft"
```

Je kunt kiezen uit verschillende stijlen: **cartoon**, **foto**, **logo** of **artistiek**. En verschillende formaten: vierkant, liggend of staand.

---

## 🧩 Onderdelen

| Onderdeel | Wat het doet |
|---|---|
| **Klantpagina Skill** | Het hoofdproces: van klantnaam naar complete Notion-pagina |
| **Nano Banana Pro** | AI-afbeeldingen genereren via Google Gemini |
| **Prompt Optimizer** | Maakt van een simpele beschrijving een professionele prompt voor de beste resultaten |
| **AI Quiz** | Interactief quiz-element voor de klantpagina |

---

## 🚀 Aan de slag

### Wat heb je nodig?

- **Python 3.8+** (voor de afbeeldingen-tool)
- **Google Gemini API key** ([gratis aanmaken](https://aistudio.google.com/apikey))

### Installatie

```bash
# Repository ophalen
git clone https://github.com/MarnieX/AiPanda-Klantpagina.git

# API key instellen
cp .env.example .env
# Open .env en vul je Gemini API key in

# Python packages installeren
pip install google-genai Pillow python-dotenv requests
```

---

## 📌 Status

🚧 In ontwikkeling (testfase)

## 📚 Documentatie

- [PLAN.md](./PLAN.md) - Architectuur, features, tech stack
- [BACKLOG.md](./BACKLOG.md) - Openstaande taken per fase
- [CHANGELOG.md](./CHANGELOG.md) - Versiegeschiedenis
- [CLAUDE.md](./CLAUDE.md) - AI-agent instructies

---

Intern project van **AI Panda** voor het automatiseren van klantprocessen.
