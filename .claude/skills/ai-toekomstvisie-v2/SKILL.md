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

Genereer twee Gamma.app presentaties van elk 10 slides die een potentiële klant een concreet en
inspirerend beeld geeft van hoe hun bedrijf er over 10 jaar uitziet met AI:

- **Presentatie 1** — AI Panda huisstijl (oranje/zwart, futuristisch)
- **Presentatie 2** — Klant huisstijl (merkkleuren + passend Gamma-thema)

Het effect dat je wilt bereiken: de klant bekijkt de presentatie en denkt
"dit zijn wij — en zo willen we zijn."

---

## Aanroep-interface (voor gebruik vanuit andere skills)

```
Input:  BEDRIJFSNAAM, SECTOR, OMSCHRIJVING, WEBSITE_DOMEIN (optioneel),
        MERKKLEUR_PRIMAIR (optioneel), MERKKLEUR_SECUNDAIR (optioneel), HUISSTIJL_KENMERK (optioneel)
Output: GAMMA_URL_1, GAMMA_URL_2 (of "niet beschikbaar" bij fallback)
```

Als alle input-variabelen al beschikbaar zijn: ga direct naar stap 1 (research).

Bekende themeId's (fallback als get_themes timet out):
- AI Panda thema: `0r1msp6zfjh4o59`

Stel bij start in:
- `GAMMA_THEME_ID_1 = "0r1msp6zfjh4o59"` (AI Panda, startwaarde)
- `GAMMA_THEME_ID_2 = ""` (klant thema, wordt ingesteld in Stap 1C)

---

## Input (alleen standalone)

Als BEDRIJFSNAAM, SECTOR of OMSCHRIJVING niet beschikbaar zijn: doe WebSearch naar de
bedrijfsnaam en lei ze af.

---

## Stap 1: Research (parallel uitvoeren)

Voer 1A, 1B en 1C tegelijkertijd uit.

### 1A — Huisstijl en merkidentiteit

**Sla deze stap over als MERKKLEUR_PRIMAIR, MERKKLEUR_SECUNDAIR én HUISSTIJL_KENMERK al meegegeven zijn vanuit de aanroepende skill.**

Als WEBSITE_DOMEIN al beschikbaar is maar de merkkleuren ontbreken: doe WebFetch op
het domein (geen WebSearch nodig). Extraheer alleen de ontbrekende waarden.

Als geen van de huisstijlvariabelen beschikbaar zijn: doe WebSearch naar `[BEDRIJFSNAAM] huisstijl merkidentiteit
kleuren logo`. Fetch daarna de homepage via WebFetch. Extraheer:
- Primaire en secundaire merkkleur(en) (hex-codes indien zichtbaar)
- Tagline of pay-off
- Sfeer van de beeldtaal: zakelijk, warm, technisch, menselijk?
- Kenmerkende visuele elementen (voertuigen, uniformen, gebouwen, materialen)

Als WEBSITE_DOMEIN niet beschikbaar is na de search: leid het af uit WebSearch-resultaten
(bijv. de domeinnaam uit een gevonden URL). Fallback: sla WEBSITE_DOMEIN op als lege string.

Sla op als: MERKKLEUR_PRIMAIR, MERKKLEUR_SECUNDAIR, HUISSTIJL_KENMERK, TAGLINE, SFEER, VISUELE_ELEMENTEN
Als MERKKLEUR_PRIMAIR niet gevonden: gebruik `#F97316` (AI Panda oranje) als standaard.

### 1B — Sectorprobleem identificeren

Doe WebSearch naar het grootste structurele probleem in SECTOR dat AI de komende 10 jaar
kan oplossen. Zoek naar fundamentele knelpunten (capaciteitstekorten, informatiefragmentatie,
veiligheidsvraagstukken, regulatoire complexiteit), niet naar kleine efficiëntiewinsten.

Sla op als: SECTORPROBLEEM (één zin die de kern beschrijft)

### 1C — Gamma thema's opzoeken (AI Panda + klant)

Stel direct in: `GAMMA_THEME_ID_1 = "0r1msp6zfjh4o59"` (het AI Panda-thema, altijd de standaard).

Roep daarna `mcp__claude_ai_Gamma__get_themes` aan om te valideren en GAMMA_THEME_ID_2 te bepalen:

**Valideer AI Panda thema (GAMMA_THEME_ID_1):**
- Succesvol: zoek naar een thema met "AI Panda" in de naam (hoofdletterongevoelig)
  - Gevonden: update GAMMA_THEME_ID_1 met het gevonden id (voor het geval het id gewijzigd is)
  - Niet gevonden: houd GAMMA_THEME_ID_1 op `"0r1msp6zfjh4o59"`
- Timeout of fout: houd GAMMA_THEME_ID_1 op `"0r1msp6zfjh4o59"`, sla klantthema-selectie over

**Selecteer klant-thema (GAMMA_THEME_ID_2) — alleen als get_themes succesvol was:**

Vertaal MERKKLEUR_PRIMAIR naar een kleurgroep:
- rood/oranje/warm: hex met R>180, G<100, B<100 → colorKeywords: ["red", "warm", "dark", "bold"]
- blauw/koel: hex met B>150, R<100 → colorKeywords: ["blue", "cool", "clean", "professional"]
- groen/natuur: hex met G>150, R<100, B<100 → colorKeywords: ["green", "nature", "organic", "fresh"]
- paars/violet: hex met R>100, B>150, G<100 → colorKeywords: ["purple", "violet", "dark", "luxe"]
- donker (zwart/donkerblauw): lage waarden voor alle channels → colorKeywords: ["dark", "onyx", "night", "deep"]
- licht/neutraal: hoge waarden voor alle channels → colorKeywords: ["light", "clean", "minimal", "neutral"]

Haal toon-keywords uit HUISSTIJL_KENMERK + SECTOR:
- "strak", "modern", "zakelijk" → toneKeywords: ["professional", "modern", "clean"]
- "warm", "menselijk", "persoonlijk" → toneKeywords: ["warm", "friendly", "human"]
- "tech", "innovatief", "digitaal" → toneKeywords: ["tech", "innovation", "digital"]
- "duurzaam", "groen", "maatschappelijk" → toneKeywords: ["sustainable", "organic", "nature"]

Doorzoek de themalijst en scoor elk thema (dat NIET "AI Panda" is):
- +2 punten per match van thema-naam/beschrijving met colorKeywords
- +1 punt per match met toneKeywords

Kies het hoogst scorende thema. Sla op als GAMMA_THEME_ID_2 en GAMMA_THEME_NAAM_2.
Als score 0 of alle thema's zijn "AI Panda": sla GAMMA_THEME_ID_2 op als `""` (Gamma kiest default).

Sla ook op als MERKKLEUR_PRIMAIR_NAAM (kleurgroep-omschrijving in het Engels, bijv. "deep red",
"royal blue", "forest green", "dark purple") — wordt gebruikt in Presentatie 2.

Log altijd:
- `"Thema 1: AI Panda (id: [GAMMA_THEME_ID_1])"`
- `"Thema 2: [GAMMA_THEME_NAAM_2] (id: [GAMMA_THEME_ID_2])"` of `"Thema 2: Gamma default (geen match)"`

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

## Stap 3: Presentatie-outlines opstellen (parallel uitvoeren)

Voer 3A en 3B tegelijkertijd uit. Sla de resultaten op als OUTLINE_1 (traject/partnership)
en OUTLINE_2 (toekomstvisie). Beide outlines worden ingevuld met specifieke content voor BEDRIJFSNAAM.

---

### 3A — Outline Presentatie 1: Traject + Partnership (AI Panda huisstijl)

Sla op als: OUTLINE_1

```
Slide 1 — Samen naar de toekomst
"[BEDRIJFSNAAM] × AI Panda"
Subtitel: [persoonlijke stelling over het partnership, max 12 woorden]
[Scene: de panda staat naast een medewerker van BEDRIJFSNAAM, schouder aan schouder,
beiden kijkend naar de horizon — team, niet verkoper]

Slide 2 — Dit zijn jullie
Kop: "[BEDRIJFSNAAM] vandaag"
OMSCHRIJVING + 3 kernfeiten + TAGLINE als pull quote
[Scene: geen panda — luchtfoto of sfeershot van locatie passend bij SECTOR]

Slide 3 — De uitdaging van vandaag
Kop: "Wat houdt [SECTOR] wakker?"
SECTORPROBLEEM in 3-4 concrete bullets voor BEDRIJFSNAAM
[Scene: panda staat bij whiteboard met frustrerende diagrammen, collega's kijken bezorgd]

Slide 4 — Waar AI het verschil maakt
Kop: "AI transformeert hoe jullie werken"
3 concrete AI-kansen specifiek voor BEDRIJFSNAAM in SECTOR
[Scene: panda en collega's kijken naar holografisch scherm met kansen en data]

Slide 5 — Wie is AI Panda?
Kop: "Jullie partner in het AI-tijdperk"
Korte introductie AI Panda: aanpak, bewezen methode.
Onderscheidend: niet alleen adviseren, maar ook daadwerkelijk implementeren.
[Scene: panda geeft presentatie — zelfverzekerd, open, uitnodigend]

Slide 6 — Onze aanpak
Kop: "Hoe we samenwerken"
AI Panda-methode in context van BEDRIJFSNAAM: wat dit per fase betekent (kort overzicht)
[Scene: panda en klantteam werken samen aan tafel, whiteboard op achtergrond]

Slide 7 — Het traject: 4 fases
Kop: "Jouw AI-reis stap voor stap"
Tijdlijn specifiek voor BEDRIJFSNAAM/SECTOR:
  Fase 1 Discovery (Week 1-2): [specifiek]
  Fase 2 Pilot (Week 3-6): [specifiek]
  Fase 3 Implementatie (Week 7-12): [specifiek]
  Fase 4 Schaling (Week 13+): [specifiek]
[Scene: panda loopt als gids voorop een kronkelend pad richting een stralend eindpunt]

Slide 8 — Wat jullie kunnen verwachten
Kop: "Concrete resultaten"
4 verwachte uitkomsten op basis van SECTOR/bedrijfstype, elk met korte duiding
Bijv: "30% tijdsbesparing" — op handmatige rapportage
[Scene: panda kijkt tevreden naar dashboard met groene resultaten]

Slide 9 — De eerste stap
Kop: "Vandaag beginnen we"
Wat er concreet als eerste gaat gebeuren (Discovery fase), klein en concreet
Tijdsinvestering: [specifiek, realistisch laagdrempelig]
[Scene: panda steekt hand uit voor handdruk richting kijker, vriendelijk en uitnodigend]

Slide 10 — Start de reis
EINDQUOTE als grote pull quote (uit Stap 2)
"Samen bouwen we aan jullie AI-toekomst."
CTA: "Plan een kennismaking → aipanda.nl"
AI Panda tagline: "Making AI Work For You"
[Scene: panda en medewerker lopen schouder aan schouder richting verlichte deur/horizon]
```

**Kwaliteitscheck OUTLINE_1:**
- Slide 5: Is "Wie is AI Panda?" genuanceerd en niet aanmatigend?
- Slide 7: Is het traject SPECIFIEK voor BEDRIJFSNAAM/SECTOR (geen generieke fases)?
- Slide 8: Zijn de verwachte resultaten REALISTISCH en sectorspecifiek?

Als een punt niet klopt: corrigeer OUTLINE_1 voordat je naar Stap 4 gaat.

---

### 3B — Outline Presentatie 2: Toekomstvisie (klant huisstijl)

Behoud de 10-slide visie-structuur maar verschuif het perspectief: de klant staat centraal,
de panda is reisleider op de achtergrond (niet hoofdrolspeler).

Sla op als: OUTLINE_2

```
Slide 1 — De toekomst van [BEDRIJFSNAAM]
Hoofdtitel: "Zo ziet [BEDRIJFSNAAM] er uit in [huidig jaar + 10]"
Subtitel: [prikkelende belofte over de transformatie, max 12 woorden — vanuit klantperspectief]
Ondertitel: Toekomstvisie [huidig jaar + 10]
[Scene: de panda staat ACHTER de medewerker, als vertrouwde gids die de weg wijst —
de medewerker kijkt naar de toekomst, de panda begeleidt]

Slide 2 — Het probleem van vandaag
Kop: "Wat houdt [SECTOR] wakker?"
SECTORPROBLEEM concreet in 3-4 bullets.
"Dit is niet een probleem van morgen. Het is het probleem van nu."
[Scene: chaotisch/druk kantoor — geen panda, puur het probleem]

Slide 3 — Jullie fundament
Kop: "Waar [BEDRIJFSNAAM] vandaan komt"
OMSCHRIJVING + 3 kernfeiten (grootte, bereik, marktpositie)
TAGLINE als pull quote — dit is WAT hen onderscheidt
[Scene: luchtfoto of wijd shot passend bij SECTOR — geen panda]

Slide 4 — Wat AI verandert
Kop: "Zo transformeert jullie manier van werken"
3 kolommen: Vandaag | Over 3 jaar | Over 10 jaar
Elk: 1 kernproces van BEDRIJFSNAAM in de SECTOR
[Scene: panda als gids naast holografisch scherm met tijdlijn-data, wijst richting toekomst]

Slide 5 — [huidig jaar + 10]: Een dag in het leven van [BEDRIJFSNAAM]
Kop: "Een gewone maandagochtend in [huidig jaar + 10]"
De openingsscène van VERHAAL_TEKST (3-4 zinnen, levendig en concreet)
[Scene: medewerker van BEDRIJFSNAAM in futuristisch kantoor, panda als vertrouwde collega op achtergrond]

Slide 6 — De doorbraak
Kop: "Het probleem dat verdween"
Hoe SECTORPROBLEEM fundamenteel veranderd is (2-3 zinnen)
Contrast: "Vroeger: [korte beschrijving] → Nu: [korte beschrijving]"
[Scene: dramatisch voor/na — panda triumfantelijk bij groene resultaten]

Slide 7 — Jullie transformatie
Kop: "Wat [BEDRIJFSNAAM] nu kan, wat concurrenten niet kunnen"
3 bullets: specifieke competitieve voordelen door AI
Marktpositie in [huidig jaar + 10]
[Scene: medewerkers van BEDRIJFSNAAM in futuristisch kantoor, panda op achtergrond als medestander]

Slide 8 — De cijfers
Kop: "De cijfers achter jullie transformatie"
4 grote getallen/feiten die letterlijk in VERHAAL_TEKST voorkomen, elk met korte duiding
[Scene: panda bij dashboard, cijfers oplichten]

Slide 9 — De reis: hoe jullie hier komen
Kop: "Van vandaag naar [huidig jaar + 10] — samen"
4 fases als tijdlijn, specifiek voor BEDRIJFSNAAM/SECTOR:
  Fase 1 Discovery (Week 1-2): [specifiek]
  Fase 2 Pilot (Week 3-6): [specifiek]
  Fase 3 Implementatie (Week 7-12): [specifiek]
  Fase 4 Schaling (Week 13+): [specifiek]
Subtiele vermelding: "AI Panda begeleidt jullie in elke stap."
[Scene: panda als reisleider voorop een pad, teamleden volgen]

Slide 10 — De uitnodiging
Kop: "Klaar voor jullie toekomst?"
EINDQUOTE als grote pull quote
Subtekst: "AI Panda begeleidt [BEDRIJFSNAAM] van visie naar werkelijkheid."
CTA: "Zet de eerste stap → aipanda.nl"
[Scene: horizon/opengedraaide deur naar het licht, panda als gids in de verte — poëtisch]
```

**Kwaliteitscheck OUTLINE_2:**
- Slide 1: Is de titel over BEDRIJFSNAAM (niet over AI Panda)?
- Slide 5: Is de scène SPECIFIEK voor dit bedrijf (niet generiek)?
- Slide 8: Komen de kerngetallen letterlijk voor in VERHAAL_TEKST?
- Is de EINDQUOTE op slide 10 dezelfde als in Stap 2?

Als een punt niet klopt: corrigeer OUTLINE_2 voordat je naar Stap 5 gaat.

---

## Stap 4: Presentatie 1 genereren — AI Panda huisstijl

**Pre-check: is Gamma beschikbaar?**

Controleer of `mcp__claude_ai_Gamma__generate` in de beschikbare tools staat. Als de tool
ontbreekt (Gamma niet gekoppeld in Claude-instellingen), sla stap 4 en 5 over en ga naar
de **Fallback** onderaan.

### 4A — Bedrijfslogo ophalen

Als WEBSITE_DOMEIN beschikbaar en niet leeg:
- Logo-URL: `https://img.logo.dev/[WEBSITE_DOMEIN]?token=pk_XpHqlOsfSNSn7E3UJB_Kmw&format=png&size=256`
- Sla op als LOGO_URL

Als WEBSITE_DOMEIN niet beschikbaar of leeg: sla LOGO_URL op als leeg.

### 4B — Basis-parameters Presentatie 1

```
inputText: [OUTLINE_1 volledig ingevuld]

numCards: 10
textOptions:
  language: "nl"
  tone: "professional"
  audience: "business executives"
imageOptions:
  source: "aiGenerated"
  model: "flux-1-pro"
  style: "photorealistic, cinematic, modern corporate.
    Recurring character: a giant panda wearing a tailored black business suit
    with an orange tie, walking and working confidently among human colleagues
    as a regular executive — the panda belongs there.
    Brand colors: #F97316 (AI Panda orange) and #000000 (black) as dominant accent colors.
    Visual style: [HUISSTIJL_KENMERK]."
additionalInstructions: "Include the AI Panda character (a giant panda in a black tailored
  business suit with orange tie) naturally on at least 7 of the 10 slides. The panda leads
  meetings, shakes hands, points at dashboards, drinks coffee, gives presentations — always
  as a confident professional among humans. Each [Scene: ...] note in the outline describes
  exactly what the panda does on that slide; follow those descriptions closely. On slides
  without a [Scene] note, choose a fitting panda moment yourself. The panda is the visual
  thread that runs through the whole presentation.
  [LOGO_INSTRUCTIE]"
```

Waarbij `[LOGO_INSTRUCTIE]`:
- Als LOGO_URL niet leeg: `"Feature the company logo ([LOGO_URL]) prominently on slide 1 (title slide) and slide 10 (closing slide) as part of the slide layout."`
- Als LOGO_URL leeg: laat dit weg.

### 4C — Fallback-keten Presentatie 1 (5 pogingen)

**Belangrijk — timeout vs. echte fout:**

De Gamma MCP-tool heeft een ingebouwde timeout (~30 seconden). Gamma-generatie duurt
vaak langer. Een timeout betekent **niet** dat de aanvraag mislukt is — het request is
al verzonden en Gamma werkt waarschijnlijk gewoon door op de achtergrond. Een nieuwe poging
na een timeout leidt dan tot dubbele presentaties.

**Na elke call — bepaal het fouttype:**

1. **Response bevat URL (begint met `https://`):** Succes. Sla op als GAMMA_URL_1, ga naar Stap 5.
2. **Timeout-fout** (foutbericht bevat "timed out", "timeout" of "time out"):
   **STOP. Niet opnieuw proberen.**
   De presentatie wordt waarschijnlijk al gegenereerd.
   Toon aan de gebruiker:
   > "De Gamma-presentatie wordt aangemaakt maar het genereren duurt langer dan verwacht.
   > Bekijk je recente presentaties op: https://gamma.app/recent"
   Sla GAMMA_URL_1 op als: `"wordt gegenereerd — check gamma.app/recent"`
   Ga naar Stap 5.
3. **Echte API-fout** (foutbericht bevat statuscode 4xx/5xx, validatiefout, of tool ontbreekt):
   Log de fout, ga naar de volgende poging met minder parameters.

---

**Poging 1 — Volledig (themeId + imageOptions met flux-1-pro):**

Parameters:
- Basis-parameters uit 4B
- `themeId: "[GAMMA_THEME_ID_1]"` (alleen als GAMMA_THEME_ID_1 niet leeg)

Na de call: pas de timeout-check hierboven toe.

---

**Poging 2 — imagen-3-pro (themeId + imageOptions, expliciete fallback):**

Alleen na echte API-fout op Poging 1.
Log: "Poging 1 mislukt. Retry met imagen-3-pro."

Parameters: basis-parameters uit 4B, maar met `imageOptions.model: "imagen-3-pro"` + `themeId` (als beschikbaar).

Na de call: pas de timeout-check hierboven toe.

---

**Poging 3 — Geen model (themeId + imageOptions, Gamma auto-select):**

Alleen na echte API-fout op Poging 2.
Log: "Poging 2 mislukt. Retry zonder model-specificatie (Gamma auto-select)."

Parameters: basis-parameters uit 4B, maar zonder `imageOptions.model` + `themeId` (als beschikbaar).

Na de call: pas de timeout-check hierboven toe.

---

**Poging 4 — Minimaal (alleen basis, geen themeId, geen imageOptions):**

Alleen na echte API-fout op Poging 3.
Log: "Poging 3 mislukt. Retry met minimale parameters."

Parameters: alleen `inputText`, `numCards: 10`, `textOptions`. Geen themeId, geen imageOptions.

Na de call: pas de timeout-check hierboven toe.

---

**Poging 5 — Markdown-fallback:**

Alleen na echte API-fout op Poging 4.
Log: "Alle Gamma-pogingen mislukt. Toon outline als Markdown."

Toon de volledige outline als gestructureerde Markdown in de chat. Meld kort:
> "Gamma is niet beschikbaar of retourneert fouten. Kopieer de onderstaande outline en plak
> hem op gamma.app → 'Nieuwe presentatie' → 'Importeer tekst'."

Sla GAMMA_URL_1 op als: `"niet beschikbaar"`

---

## Stap 5: Presentatie 2 genereren — Klant huisstijl

**Overslaan-conditie:**
Als `MERKKLEUR_PRIMAIR = "#F97316"` (of niet ingesteld / default AI Panda oranje): sla deze
stap volledig over. Er is geen zinvol verschil met Presentatie 1.
Log: "Stap 5 overgeslagen: merkkleur is AI Panda default."
Sla GAMMA_URL_2 op als: `"overgeslagen (zelfde als Presentatie 1)"`

---

**Basis-parameters Presentatie 2:**

```
inputText: [OUTLINE_2 volledig ingevuld, met VERHAAL_TEKST ingevuld op slide 5]

numCards: 10
textOptions:
  language: "nl"
  tone: "professional"
  audience: "business executives"
imageOptions:
  source: "aiGenerated"
  model: "flux-1-pro"
  style: "photorealistic, cinematic, modern corporate.
    Recurring character: a giant panda wearing a tailored black business suit
    with a [MERKKLEUR_PRIMAIR_NAAM]-colored tie (hex: [MERKKLEUR_PRIMAIR]),
    walking and working confidently among human colleagues as a regular
    executive — the panda belongs there.
    Brand colors: [MERKKLEUR_PRIMAIR] (primary) and [MERKKLEUR_SECUNDAIR]
    (secondary) as accent colors throughout.
    Visual style: [HUISSTIJL_KENMERK]."
additionalInstructions: "Include the AI Panda character (a giant panda in a black tailored
  business suit with a [MERKKLEUR_PRIMAIR_NAAM]-colored tie) naturally on at least 7 of the
  10 slides. The panda leads meetings, shakes hands, points at dashboards, drinks coffee,
  gives presentations — always as a confident professional among humans. Each [Scene: ...]
  note in the outline describes exactly what the panda does on that slide; follow those
  descriptions closely. On slides without a [Scene] note, choose a fitting panda moment
  yourself. The panda is the visual thread that runs through the whole presentation.
  Use the brand colors [MERKKLEUR_PRIMAIR] and [MERKKLEUR_SECUNDAIR] as dominant accent
  colors in environments, lighting, and design elements.
  Incorporate the visual style '[HUISSTIJL_KENMERK]' in the overall aesthetic.
  [LOGO_INSTRUCTIE]"
```

Waarbij `[LOGO_INSTRUCTIE]` dezelfde logica volgt als in Stap 4B.

**themeId:** GAMMA_THEME_ID_2 (als niet leeg; anders geen themeId opgeven).

**Na elke call — zelfde timeout-check als Stap 4C:**

1. Response bevat URL: succes. Sla op als GAMMA_URL_2, ga naar Stap 6.
2. Timeout-fout: STOP. Sla op als `"wordt gegenereerd — check gamma.app/recent"`. Ga naar Stap 6.
3. Echte API-fout: ga naar volgende poging.

---

**Poging 1 — Volledig (themeId + imageOptions met flux-1-pro):**

Parameters: basis-parameters Presentatie 2 + `themeId: "[GAMMA_THEME_ID_2]"` (als niet leeg).

---

**Poging 2 — imagen-3-pro (themeId + imageOptions, expliciete fallback):**

Alleen na echte API-fout op Poging 1.
Log: "Presentatie 2 Poging 1 mislukt. Retry met imagen-3-pro."

Parameters: basis-parameters Presentatie 2, maar met `imageOptions.model: "imagen-3-pro"` + `themeId` (als beschikbaar).

---

**Poging 3 — Geen model (themeId + imageOptions, Gamma auto-select):**

Alleen na echte API-fout op Poging 2.
Log: "Presentatie 2 Poging 2 mislukt. Retry zonder model-specificatie."

Parameters: basis-parameters Presentatie 2, maar zonder `imageOptions.model` + `themeId` (als beschikbaar).

---

**Poging 4 — Minimaal (geen themeId, geen imageOptions):**

Alleen na echte API-fout op Poging 3.
Log: "Presentatie 2 Poging 3 mislukt. Retry met minimale parameters."

Parameters: alleen `inputText`, `numCards: 10`, `textOptions`.

---

**Poging 5 — Melding:**

Alleen na echte API-fout op Poging 4.
Log: "Presentatie 2 alle pogingen mislukt."

Sla GAMMA_URL_2 op als: `"niet beschikbaar — gebruik Presentatie 1"`

---

## Stap 6: Resultaat tonen

**Als beide presentaties geslaagd:**

```
## Toekomstvisie presentaties klaar voor [BEDRIJFSNAAM]

**Presentatie 1 — AI Panda huisstijl:**
→ [GAMMA_URL_1]

**Presentatie 2 — [BEDRIJFSNAAM] huisstijl:**
→ [GAMMA_URL_2]

Slide-overzicht: [titels slide 1–10]
Sectorprobleem: [SECTORPROBLEEM]
Eindquote: "[EINDQUOTE]" — [QUOTE_PERSOON]
```

**Als Presentatie 2 overgeslagen (default kleuren):**

Toon alleen Presentatie 1 met melding:
> "Presentatie 2 is overgeslagen omdat de merkkleuren overeenkomen met de AI Panda huisstijl.
> Presentatie 1 is de definitieve versie."

**Als Presentatie 1 of 2 "niet beschikbaar":**

Toon beschikbare URL's + melding welke mislukt is + fallback-instructie (gamma.app/recent of markdown-outline).

**Als Gamma volledig niet beschikbaar (fallback gebruikt):**

Toon de volledige outline als Markdown.
Geef daarna ook mee:
- Welk thema aanbevolen wordt op gamma.app: zoek op "AI Panda" of "Canaveral"
- Kort: welk sectorprobleem als kern is gekozen en de EINDQUOTE

---

## Foutafhandeling

- Research faalt → gebruik eigen sectorkennis, meld dit
- MERKKLEUR_PRIMAIR niet gevonden → gebruik AI Panda oranje (#F97316) als accentkleur
- WEBSITE_DOMEIN niet beschikbaar → sla logo-stap over, ga door zonder logo-instructie
- Gamma niet beschikbaar (tool ontbreekt) → toon outline als Markdown, verwijs naar gamma.app
- get_themes faalt of timet out → gebruik hardcoded GAMMA_THEME_ID_1 `"0r1msp6zfjh4o59"`, GAMMA_THEME_ID_2 `""`
- Gamma retourneert geen URL → retry met progressief minder parameters (zie 4C / Stap 5)
