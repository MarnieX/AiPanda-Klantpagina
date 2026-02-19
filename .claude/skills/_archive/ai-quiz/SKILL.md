---
name: ai-quiz
description: "Genereer een interactieve AI-Readiness Quickscan quiz voor een bedrijf. Bouwt een klikbare quiz-URL en embed deze in een Notion-pagina."
---

# AI-Readiness Quiz Generator (Interactief)

Deze skill genereert een interactieve AI-Readiness Quickscan: een klikbare quiz die in de browser draait. De vragen worden als JSON meegegeven in de URL, zodat geen server nodig is.

## Configuratie

```
QUIZ_BASE_URL = https://marniex.github.io/aipanda-quiz
```

> **Let op:** Als de GitHub Pages URL nog niet live is, gebruik dan de lokale `quiz/index.html` voor testen.

## Input

De skill verwacht de volgende contextvariabelen (of vraagt erom als ze ontbreken):
- `BEDRIJFSNAAM` (bijv. "Coolblue")
- `SECTOR` (bijv. "Retail")

Als deze niet beschikbaar zijn, vraag erom via `AskUserQuestion`.

---

## Stap 1: Genereer quizvragen

Genereer 5 meerkeuzevragen specifiek voor `[BEDRIJFSNAAM]` in de sector `[SECTOR]`.

**Structuur per vraag:**
- Vraagstelling (helder en direct)
- 3 Antwoordopties (A/B/C) oplopend in volwassenheid (A=Start, B=Groei, C=Leider)
- Scoring: A = 1 punt, B = 2 punten, C = 3 punten

**Inhoudelijke focus:**
1. **Algemeen:** Hoe wordt AI nu gebruikt in dagelijkse processen?
2. **Data:** Hoe is data in de `[SECTOR]` georganiseerd? (Noem specifieke data zoals patiëntdossiers, kassabonnen of logistieke logs).
3. **Proces:** Welke `[SECTOR]`-processen zijn geautomatiseerd? (Noem specifieke processen zoals roostering, orderpicking of triage).
4. **Team:** Hoe staat het team tegenover werken met AI-tools?
5. **Strategie:** Wat is de strategische visie op AI?

**Tone-of-voice:**
- Schrijf de vragen en antwoorden direct aan de klant
- Zorg dat de toon uitnodigend is en niet als een examen aanvoelt
- Antwoord A is niet 'fout', maar een startpunt met potentie
- Gebruik vakterminologie die past bij de sector

---

## Stap 2: Structureer als JSON

Zet de gegenereerde vragen om naar het volgende JSON-formaat:

```json
{
  "bedrijf": "[BEDRIJFSNAAM]",
  "sector": "[SECTOR]",
  "vragen": [
    {
      "vraag": "Hoe wordt AI nu gebruikt in jullie dagelijkse processen?",
      "opties": [
        {"label": "A", "tekst": "We gebruiken nog geen AI-tools", "score": 1},
        {"label": "B", "tekst": "Enkele medewerkers experimenteren", "score": 2},
        {"label": "C", "tekst": "AI is structureel ingebed", "score": 3}
      ]
    }
  ]
}
```

Sla op als `QUIZ_JSON`.

---

## Stap 3: Base64-encode en bouw de URL

Encodeer de JSON naar een base64 string en bouw de volledige quiz-URL:

```bash
QUIZ_BASE_URL="https://marniex.github.io/aipanda-quiz"
QUIZ_JSON='[DE GEGENEREERDE JSON]'

# Base64-encode (URL-safe)
B64=$(echo -n "$QUIZ_JSON" | base64 | tr -d '\n')

# Bouw de volledige URL
QUIZ_URL="${QUIZ_BASE_URL}/#data=${B64}"

echo "$QUIZ_URL"
```

Sla het resultaat op als `QUIZ_URL`.

**Verificatie:** Decodeer de base64 terug om te controleren dat de JSON intact is:
```bash
echo "$B64" | base64 -d
```

---

## Stap 4: Maak Notion-pagina aan

Gebruik `notion-create-pages` om een quiz-pagina aan te maken.

**Als er een `PARENT_PAGE_ID` beschikbaar is** (bijv. vanuit de klantpagina-skill): maak de pagina aan als sub-pagina met `page_id: PARENT_PAGE_ID`.

**Titel:** `AI-Readiness Quickscan — [BEDRIJFSNAAM]`

**Content:**

```markdown
# AI-Readiness Quickscan

Ontdek hoe ver [BEDRIJFSNAAM] staat op het gebied van AI. Beantwoord 5 korte vragen en krijg direct je AI-volwassenheidsprofiel.

---

## Start de quiz

Klik op de link hieronder om de interactieve quiz te openen:

[Start de AI-Readiness Quickscan]([QUIZ_URL])

---

## Hoe werkt het?

Beantwoord 5 meerkeuzevragen over AI-gebruik binnen [BEDRIJFSNAAM]. Per vraag kies je het antwoord dat het beste bij jullie huidige situatie past. Na de laatste vraag zie je direct:

- **Je score** (op een schaal van 5-15)
- **Je profiel** (van Starter tot Koploper)
- **Een toelichting** met concrete vervolgstappen

## Score-profielen

| Score | Profiel | Wat dit betekent |
|---|---|---|
| 5-7 | De Starter | Jullie staan aan het begin. Focus op bewustwording en laaghangend fruit. |
| 8-9 | De Verkenner | De interesse is er. Tijd voor structuur en strategie. |
| 10-11 | De Groeier | De basis staat. Klaar voor serieuze pilot-projecten. |
| 12-13 | De Versneller | Jullie gaan hard. Opschalen van successen naar bedrijfsbreed. |
| 14-15 | De Koploper | AI zit in jullie DNA. Focus op innovatie en voorsprong. |

---

*Gegenereerd door AI Panda*
```

**Sla het `id` uit de response op als `QUIZ_PAGE_ID`.**

---

## Stap 5: Toon resultaat

Toon aan de gebruiker:
1. De quiz-URL (klikbaar)
2. De Notion-pagina URL (als beschikbaar)
3. Korte bevestiging: "Interactieve quiz aangemaakt voor [BEDRIJFSNAAM]"

Sla op:
- `QUIZ_URL` — de directe link naar de interactieve quiz
- `QUIZ_PAGE_ID` — het Notion page ID (voor gebruik door andere skills)

---

## Foutafhandeling

- Base64-encoding faalt → probeer Python als alternatief:
  ```bash
  python3 -c "import base64, json; print(base64.b64encode(json.dumps([DATA]).encode()).decode())"
  ```
- Notion-pagina aanmaken faalt → toon alleen de quiz-URL als resultaat. GA ALTIJD DOOR.
- Quiz-URL is te lang → dit zou niet moeten voorkomen (hash fragment heeft geen server-side limiet), maar als het toch faalt: verkort de vraagteksten.

---

## Integratie met klantpagina-skill

Wanneer deze skill wordt aangeroepen vanuit de klantpagina-skill (stap 5C/6B):
- De klantpagina-skill levert `BEDRIJFSNAAM`, `SECTOR` en `PARENT_PAGE_ID`
- Deze skill levert `QUIZ_URL` en `QUIZ_PAGE_ID` terug
- De klantpagina-skill kan de `QUIZ_URL` embedden in de hoofdpagina
