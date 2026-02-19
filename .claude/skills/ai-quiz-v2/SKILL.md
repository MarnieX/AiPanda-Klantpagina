---
name: ai-quiz-v2
description: "Genereer een interactieve AI-Readiness Quickscan quiz voor een bedrijf. Bouwt een klikbare quiz-URL. Werkt standalone (met Notion-pagina) en in quick mode (vanuit andere skills, zonder Notion)."
---

# AI-Readiness Quiz Generator v2

Genereer een interactieve AI-Readiness Quickscan: een klikbare quiz die in de browser draait. De vragen worden als JSON meegegeven in de URL, zodat geen server nodig is.

## Configuratie

```
QUIZ_BASE_URL = https://marniex.github.io/aipanda-quiz
```

---

## Aanroep-interface (voor gebruik vanuit andere skills)

```
Input:  BEDRIJFSNAAM, SECTOR
Output: QUIZ_URL
```

Als BEDRIJFSNAAM en SECTOR al beschikbaar zijn: sla input-vragen over, ga direct naar stap 1 (vragen genereren). Sla ook stap 4 (Notion-pagina) over wanneer aangeroepen vanuit een andere skill (PARENT_SKILL is gezet).

---

## Input (alleen standalone)

Als BEDRIJFSNAAM of SECTOR niet beschikbaar zijn, vraag erom via AskUserQuestion.

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

**Primaire methode (Python, werkt overal):**

```bash
QUIZ_URL=$(python3 -c "
import base64, json, sys
data = '''[QUIZ_JSON]'''
b64 = base64.b64encode(data.encode()).decode()
print(f'https://marniex.github.io/aipanda-quiz/#data={b64}')
")
echo "$QUIZ_URL"
```

**Alternatieve methode (bash):**

```bash
QUIZ_BASE_URL="https://marniex.github.io/aipanda-quiz"
QUIZ_JSON='[DE GEGENEREERDE JSON]'
B64=$(echo -n "$QUIZ_JSON" | base64 | tr -d '\n')
QUIZ_URL="${QUIZ_BASE_URL}/#data=${B64}"
echo "$QUIZ_URL"
```

**Verificatie:** Decodeer de base64 terug om te controleren dat de JSON intact is:
```bash
echo "$B64" | base64 -d | python3 -m json.tool
```

Sla het resultaat op als `QUIZ_URL`.

---

## Stap 4: Notion-pagina aanmaken (optioneel)

**Alleen uitvoeren als de skill standalone draait (niet vanuit een andere skill).** Controleer: als PARENT_SKILL is gezet, sla deze stap over.

Gebruik `notion-create-pages` om een quiz-pagina aan te maken.

**Als er een `PARENT_PAGE_ID` beschikbaar is:** maak de pagina aan als sub-pagina met `page_id: PARENT_PAGE_ID`.

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
2. De Notion-pagina URL (als aangemaakt)
3. Korte bevestiging: "Interactieve quiz aangemaakt voor [BEDRIJFSNAAM]"

Sla op:
- `QUIZ_URL` — de directe link naar de interactieve quiz
- `QUIZ_PAGE_ID` — het Notion page ID (indien aangemaakt)

---

## Foutafhandeling

- Base64-encoding faalt (bash) → gebruik Python-methode (stap 3 primaire methode)
- Notion-pagina aanmaken faalt → toon alleen de quiz-URL als resultaat. GA ALTIJD DOOR.
- Quiz-URL is te lang → verkort de vraagteksten
