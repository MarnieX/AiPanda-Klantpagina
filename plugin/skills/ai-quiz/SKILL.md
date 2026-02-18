---
name: ai-quiz
description: "Genereer een AI-Readiness Quickscan quiz specifiek voor een bedrijf en sector."
---

# AI-Readiness Quiz Generator

Deze skill genereert 5 meerkeuzevragen voor de "AI-Readiness Quickscan" specifiek voor een opgegeven bedrijf en sector.

## Input

De skill verwacht de volgende contextvariabelen (of vraagt erom als ze ontbreken):
- `BEDRIJFSNAAM` (bijv. "Coolblue")
- `SECTOR` (bijv. "Retail")

Als deze niet beschikbaar zijn, vraag erom via `AskUserQuestion`.

## Stap 1: Genereer Quiz

Genereer 5 meerkeuzevragen specifiek voor `[BEDRIJFSNAAM]` in de sector `[SECTOR]`.

**Structuur per vraag:**
- Vraagstelling (Bold)
- 3 Antwoordopties (A/B/C) oplopend in volwassenheid (A=Start, B=Groei, C=Leider).

**Inhoudelijke focus:**
1. **Algemeen:** Hoe wordt AI nu gebruikt in dagelijkse processen?
2. **Data:** Hoe is data in de `[SECTOR]` georganiseerd? (Noem specifieke data zoals patiëntdossiers, kassabonnen of logistieke logs).
3. **Proces:** Welke `[SECTOR]`-processen zijn geautomatiseerd? (Noem specifieke processen zoals roostering, orderpicking of triage).
4. **Team:** Hoe staat het team tegenover werken met AI-tools?
5. **Strategie:** Wat is de strategische visie op AI?

**Tone-of-voice:**
- Schrijf de vragen en antwoorden direct aan de klant.
- Zorg dat de toon uitnodigend is en niet als een examen aanvoelt.
- Antwoord A is niet 'fout', maar een startpunt met potentie.
- Gebruik vakterminologie die past bij de sector.

## Stap 2: Output

Toon de gegenereerde quiz in Markdown formaat en sla deze op in de variabele `QUIZ_VRAGEN`.
