# AI Panda - Klantpagina Generator

> Van klantnaam naar complete Notion-pagina in een paar seconden.

AI Panda helpt consultants om razendsnel professionele klantpagina's aan te maken in Notion. Geen handmatig kopieerwerk, geen losse templates. Je geeft een bedrijfsnaam op en de rest gebeurt automatisch.

---

## Wat doet het?

**Het probleem:** Voor elke nieuwe klant maak je handmatig een Notion-pagina aan. Bedrijfsinfo opzoeken, afbeelding zoeken of maken, template invullen, roadmap aanmaken. Dat kost tijd en ziet er niet altijd consistent uit.

**De oplossing:** Deze tool automatiseert het hele proces:

1. **Bedrijfsinfo ophalen** - Haalt automatisch relevante informatie op van de website van de klant
2. **Team koppelen** - Leest de beschikbare consultants uit het teambestand en koppelt de juiste mensen
3. **Unieke afbeelding genereren** - Maakt met AI (Google Gemini) een op maat gemaakte afbeelding in de AI Panda-stijl
4. **Notion-pagina bouwen** - Zet alles samen in een professionele klantpagina, compleet met roadmap en projectstructuur

Het resultaat: een consistente, professionele uitstraling voor elke klant, zonder handwerk.

---

## Hoe werkt het?

### Via Claude Code (aanbevolen)

Typ simpelweg `/klantpagina` in Claude Code en volg de stappen. Claude vraagt om de klantnaam, haalt alles op en maakt de pagina aan.

### De afbeeldingen-tool los gebruiken

Wil je alleen een afbeelding genereren (bijvoorbeeld voor een presentatie of social post)? Dat kan ook los:

```
./banana.sh "een panda die code schrijft"
```

Je kunt kiezen uit verschillende stijlen: **cartoon**, **foto**, **logo** of **artistiek**. En verschillende formaten: vierkant, liggend of staand.

---

## Onderdelen

| Onderdeel | Wat het doet |
|---|---|
| **Klantpagina Skill** | Het hoofdproces: van klantnaam naar complete Notion-pagina |
| **Nano Banana Pro** | AI-afbeeldingen genereren via Google Gemini |
| **Prompt Optimizer** | Maakt van een simpele beschrijving een professionele prompt voor de beste resultaten |
| **MCP Plugin** | Integratie met Claude Desktop zodat je de tools direct vanuit Claude kunt gebruiken |

---

## Aan de slag

### Wat heb je nodig?

- **Python 3.8+** (voor de afbeeldingen-tool)
- **Google Gemini API key** ([gratis aanmaken](https://aistudio.google.com/apikey))
- **Node.js** (alleen als je de Claude Desktop plugin wilt gebruiken)

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

### Claude Desktop plugin (optioneel)

```bash
./setup-nano-banana-mcp.sh
```

Dit script configureert alles automatisch. Na het herstarten van Claude Desktop kun je direct afbeeldingen genereren vanuit een gesprek.

---

## Gemaakt door

Intern project van **AI Panda / Marnit** voor het automatiseren van klantprocessen.
