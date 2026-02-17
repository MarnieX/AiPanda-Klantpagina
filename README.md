# 🐼 AI Panda - Klantpagina Generator

> Van klantnaam naar complete Notion-pagina in een paar seconden.

Met de Klantpagina Generator maken consultants van **AI Panda** razendsnel professionele klantpagina's aan in Notion. Geen handmatig kopieerwerk, geen losse templates. Geef een bedrijfsnaam op en de rest gebeurt automatisch.

---

## 🎯 Wat doet het?

**Het probleem:** Voor elke nieuwe klant maak je handmatig een Notion-pagina aan. Bedrijfsinfo opzoeken, afbeelding zoeken of maken, template invullen, roadmap aanmaken. Dat kost tijd en ziet er niet altijd consistent uit.

**De oplossing:** Deze plugin automatiseert het hele proces. Je typt `/klantpagina` in Claude Cowork, geeft een bedrijfsnaam op, en binnen een paar seconden staat er een complete, professionele klantpagina in Notion.

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

## 🚀 Aan de slag

### Stap 1: Plugin installeren in Claude Cowork

Download het plugin-bestand (`ai-panda-klantpagina.plugin`) uit deze repository en installeer het in Claude Cowork:

1. Open **Claude Cowork**
2. Ga naar **Instellingen** > **Plugins**
3. Klik op **Plugin toevoegen** en selecteer het `.plugin` bestand
4. De plugin is nu beschikbaar in je Cowork-omgeving

### Stap 2: API-keys instellen

De plugin maakt gebruik van externe services. Je moet de volgende API-keys instellen op je eigen computer:

| Key | Waarvoor | Waar aan te maken |
|---|---|---|
| `GEMINI_API_KEY` | AI-beeldgeneratie (verplicht) | [Google AI Studio](https://aistudio.google.com/apikey) (gratis) |
| `CLOUDINARY_CLOUD_NAME` | Image hosting (optioneel) | [Cloudinary](https://cloudinary.com/users/register_free) |
| `CLOUDINARY_API_KEY` | Image hosting (optioneel) | Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | Image hosting (optioneel) | Cloudinary dashboard |

Maak een `.env` bestand aan in je projectfolder (gebruik `.env.example` als voorbeeld):

```bash
cp .env.example .env
# Open .env en vul je API-keys in
```

### Stap 3: Klantpagina genereren

Typ `/klantpagina` in Claude Cowork en volg de stappen. Claude vraagt om de klantnaam, haalt de bedrijfsinfo op, genereert een afbeelding en maakt de Notion-pagina aan.

---

## 🧩 Onderdelen

| Onderdeel | Wat het doet |
|---|---|
| **Klantpagina Skill** | Het hoofdproces: van klantnaam naar complete Notion-pagina |
| **Nano Banana Pro** | AI-afbeeldingen genereren via Google Gemini |
| **Prompt Optimizer** | Maakt van een simpele beschrijving een professionele prompt voor de beste resultaten |
| **AI Quiz** | Interactief quiz-element voor de klantpagina |

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
