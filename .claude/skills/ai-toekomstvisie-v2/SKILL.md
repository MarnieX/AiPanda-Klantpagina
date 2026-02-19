---
name: ai-toekomstvisie-v2
description: >
  Genereer een visionaire AI-toekomstvisie voor een klant als Gamma.app presentatie van 10 slides
  in de AI Panda huisstijl. Schrijft een inspirerend 10-jaar transformatieverhaal en bouwt
  hiervan een professionele pitch-presentatie.

  Aanroepen vanuit de klantpagina-skill na het aanmaken van de Notion-pagina, of standalone met:
  "maak een toekomstvisie voor [bedrijf]", "gamma presentatie voor [klant]".
---

# AI Toekomstvisie — Gamma Presentatie v2

## Doel

Genereer een Gamma.app presentatie van 10 slides die een potentiële klant een concreet en
inspirerend beeld geeft van hoe hun bedrijf er over 10 jaar uitziet met AI. De presentatie
gebruikt de AI Panda huisstijl (oranje/zwart, futuristisch) en is geschikt als pitch-deck
of opvolgmateriaal na een eerste gesprek.

Het effect dat je wilt bereiken: de klant bekijkt de presentatie en denkt
"dit zijn wij — en zo willen we zijn."

---

## Aanroep-interface (voor gebruik vanuit andere skills)

```
Input:  BEDRIJFSNAAM, SECTOR, OMSCHRIJVING
Output: GAMMA_URL (of "niet beschikbaar" bij fallback)
```

Als alle input-variabelen al beschikbaar zijn: ga direct naar stap 1 (research).

---

## Input (alleen standalone)

Als BEDRIJFSNAAM, SECTOR of OMSCHRIJVING niet beschikbaar zijn: doe WebSearch naar de
bedrijfsnaam en lei ze af.

---

## Stap 1: Research (parallel uitvoeren)

### 1A — Huisstijl en merkidentiteit
Doe WebSearch naar `[BEDRIJFSNAAM] huisstijl merkidentiteit kleuren logo`. Fetch daarna
de homepage via WebFetch. Extraheer:
- Primaire en secundaire merkkleur(en) (hex-codes indien zichtbaar)
- Tagline of pay-off
- Sfeer van de beeldtaal: zakelijk, warm, technisch, menselijk?
- Kenmerkende visuele elementen (voertuigen, uniformen, gebouwen, materialen)

Sla op als: MERKKLEUR_PRIMAIR, MERKKLEUR_SECUNDAIR, TAGLINE, SFEER, VISUELE_ELEMENTEN

### 1B — Sectorprobleem identificeren
Doe WebSearch naar het grootste structurele probleem in SECTOR dat AI de komende 10 jaar
kan oplossen. Zoek naar fundamentele knelpunten (capaciteitstekorten, informatiefragmentatie,
veiligheidsvraagstukken, regulatoire complexiteit), niet naar kleine efficiëntiewinsten.

Sla op als: SECTORPROBLEEM (één zin die de kern beschrijft)

---

## Stap 2: Verhaal schrijven

Schrijf een visionair transformatieverhaal van 300-400 woorden in het Nederlands.

**Structuur** (doorlopend proza, geen kopjes):

1. **Opening met een persoon** — een medewerker op een werkdag in [huidig jaar + 10].
   Specifiek: naam, functie, wat ze ziet en doet. Voelt als een scène.

2. **Sectorprobleem opgelost** — hoe het SECTORPROBLEEM er destijds uitzag en hoe AI
   dit nu fundamenteel heeft opgelost. Dit is het visionaire hart.

3. **Bedrijfsbrede transformatie** — hoe staat BEDRIJFSNAAM er voor in de markt?
   Wat kunnen ze nu wat niemand anders kan?

4. **Terug naar de mens** — eindquote van de persoon uit de opening. Kort, concreet.
   Formaat: *"[quote]"* — [Voornaam], [functie] bij BEDRIJFSNAAM, [huidig jaar + 10]

**Toon**: Warm, visionair, geloofwaardig. Niet wollig of generiek. Geen sciencefiction.

Sla op als: VERHAAL_TEKST, EINDQUOTE, QUOTE_PERSOON (naam + functie)

---

## Stap 3: Presentatie-outline opstellen + kwaliteitscheck

Stel een gedetailleerde outline op voor 10 slides. Gebruik de vaste structuur hieronder
en vul elk onderdeel in met specifieke content voor BEDRIJFSNAAM.

```
Slide 1 — Titel
"AI Panda x [BEDRIJFSNAAM]"
Subtitel: [prikkelende stelling over de transformatie, max 12 woorden]
Ondertitel: Toekomstvisie [huidig jaar + 10] | AI Panda

Slide 2 — Het probleem van vandaag
Kop: "Wat houdt [SECTOR] wakker?"
Beschrijf het SECTORPROBLEEM concreet in 3-4 bullets.
Sluit af: "Dit is niet een probleem van morgen. Het is het probleem van nu."

Slide 3 — Wie is [BEDRIJFSNAAM]?
Kop: "[BEDRIJFSNAAM] in één oogopslag"
OMSCHRIJVING + 3 kernfeiten (grootte, bereik, marktpositie indien bekend)
TAGLINE als pull quote

Slide 4 — Wat AI verandert
Kop: "AI is geen tool. Het is een nieuwe manier van werken."
3 kolommen: Vandaag | Over 3 jaar | Over 10 jaar
Elk: 1 kernproces van BEDRIJFSNAAM in de SECTOR

Slide 5 — 2035: Een dag in het leven
Kop: "Een gewone maandagochtend in [huidig jaar + 10]"
De openingsscène van het verhaal (3-4 zinnen, levendig en concreet)
Foto-prompt voor Gemini: hyperrealistisch, MERKKLEUR_PRIMAIR als accent, medewerker in beeld

Slide 6 — De doorbraak
Kop: "Het probleem dat AI oploste"
Beschrijf hoe het SECTORPROBLEEM fundamenteel is veranderd (2-3 zinnen)
Contrast: "Vroeger: [korte beschrijving] → Nu: [korte beschrijving]"

Slide 7 — Bedrijfsbrede transformatie
Kop: "Wat [BEDRIJFSNAAM] nu kan, wat concurrenten niet kunnen"
3 bullets: specifieke competitieve voordelen die door AI zijn ontstaan
Afsluit met marktpositie in [huidig jaar + 10]

Slide 8 — Kerngetallen
Kop: "De cijfers achter de transformatie"
4 grote getallen/feiten die letterlijk in het verhaal voorkomen
Elk getal met 1 korte duiding (bijv: "3x sneller" — klantresponstijd gehalveerd)

Slide 9 — De roadmap
Kop: "Van hier naar daar — met AI Panda"
4 fases als tijdlijn:
  Fase 1 Discovery (Week 1-2): [specifiek voor BEDRIJFSNAAM/SECTOR]
  Fase 2 Pilot (Week 3-6): [specifiek]
  Fase 3 Implementatie (Week 7-12): [specifiek]
  Fase 4 Schaling (Week 13+): [specifiek]

Slide 10 — De eerste stap
Kop: "Klaar om te beginnen?"
EINDQUOTE als grote pull quote
Subtekst: "AI Panda begeleidt [BEDRIJFSNAAM] van visie naar werkelijkheid."
CTA: "Plan een kennismaking → aipanda.nl"
AI Panda tagline: "Making AI Work For You"
```

**Kwaliteitscheck (controleer voordat je naar stap 4 gaat):**

- Is de **prikkelende stelling** op slide 1 specifiek voor dit bedrijf (niet generiek)?
- Beschrijft slide 5 iets wat **vandaag nog niet bestaat**?
- Zit het **SECTORPROBLEEM** verwerkt in slide 2 én slide 6?
- Komen de **kerngetallen** op slide 8 letterlijk voor in het verhaal?
- Staat de **EINDQUOTE** letterlijk op slide 10?
- Is de roadmap op slide 9 **specifiek** voor SECTOR en BEDRIJFSNAAM?

Als een punt niet klopt: corrigeer de outline voordat je doorgaat.

---

## Stap 4: Gamma presentatie genereren

**Pre-check: is Gamma beschikbaar?**

Controleer of `mcp__claude_ai_Gamma__generate` in de beschikbare tools staat. Als de tool
ontbreekt (Gamma niet gekoppeld in Claude-instellingen), sla deze stap over en ga naar
de **Fallback** onderaan.

**Gemeenschappelijke parameters (gebruik bij alle pogingen):**
```
inputText: [de volledige outline uit Stap 3 + de volledige VERHAAL_TEKST ingevuld op slide 5]
numCards: 10
textOptions:
  language: "nl"
  tone: "professional"
  audience: "business executives"
imageOptions:
  source: "aiGenerated"
  style: "photorealistic, cinematic, modern office"
```

**Let op:** Geef de volledige, uitgeschreven outline mee als `inputText`. Niet een samenvatting.

**Poging 1 — AI Panda custom theme:**
Voeg toe: `themeId: "0r1msp6zfjh4o59"` (oranje/zwart/futuristisch).

Als Poging 1 mislukt door een onbekend themeId-fout, ga naar Poging 2.

**Poging 2 — Canaveral theme (fallback):**
Vervang themeId door: `themeId: "canaveral"`.

Als Poging 2 ook mislukt, ga naar Poging 3.

**Poging 3 — Geen themeId (Gamma default):**
Verwijder de themeId parameter volledig.

**Fallback (Gamma niet beschikbaar of alle pogingen falen):**
Toon de volledige outline als gestructureerde Markdown in de chat. Meld kort:
> "Gamma is niet beschikbaar in deze omgeving. Kopieer de onderstaande outline en plak
> hem op gamma.app → 'Nieuwe presentatie' → 'Importeer tekst'."

Sla de teruggegeven URL op als: GAMMA_URL (of GAMMA_URL = "niet beschikbaar" bij fallback)

---

## Stap 5: Resultaat tonen

**Als Gamma geslaagd:**
Toon aan de gebruiker:
1. **Gamma presentatie**: [GAMMA_URL] (klikbaar)
2. Kort overzicht van de 10 slides (titel per slide)
3. Het sectorprobleem dat als kern is gekozen
4. De EINDQUOTE die als pull quote op slide 10 staat

**Als Gamma niet beschikbaar (fallback gebruikt):**
Toon de volledige outline als Markdown.
Geef daarna ook mee:
- Welk thema aanbevolen wordt op gamma.app: zoek op "Canaveral" of "AI Panda"
- Kort: welk sectorprobleem als kern is gekozen en de EINDQUOTE

---

## Foutafhandeling

- Research faalt → gebruik eigen sectorkennis, meld dit
- Merkkleur niet gevonden → gebruik AI Panda oranje (#F97316) als accentkleur
- Gamma niet beschikbaar (tool ontbreekt) → toon outline als Markdown, verwijs naar gamma.app
- Gamma themeId `0r1msp6zfjh4o59` onbekend → retry met `canaveral` → retry zonder themeId
- Gamma retourneert fout → toon outline als Markdown, meld de fout kort
