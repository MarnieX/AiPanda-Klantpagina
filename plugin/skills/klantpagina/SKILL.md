---
name: klantpagina
description: "Genereer een professionele Notion-klantpagina voor AI Panda. Haalt bedrijfsinfo op van de website, leest consultants uit een Excel, genereert een AI Panda-afbeelding en maakt een complete Notion-pagina met roadmap."
---

# AI Panda Klantpagina Generator

Je genereert een professionele Notion-klantpagina voor AI Panda. Volg de stappen exact in volgorde.

Gebruik TodoWrite om je voortgang te tonen met deze stappen:
1. Klant-URL ophalen
2. Bedrijfsinfo ophalen van website
3. AI Panda team inlezen uit Excel
4. Consultants laten kiezen
5. AI Panda-afbeelding genereren
6. Notion-pagina aanmaken
7. Resultaat bevestigen

---

## Stap 1: Vraag om de klant

Gebruik AskUserQuestion:
- question: "Voor welk bedrijf wil je een AI Panda klantpagina genereren?"
- header: "Klant"
- Bied 3 voorbeeldbedrijven als opties (bijv. Coolblue, bol.com, Jumbo) — de gebruiker kan ook via "Other" een eigen URL/naam typen.
- multiSelect: false

## Stap 2: Haal bedrijfsinformatie op

Probeer EERST WebFetch op de website van het bedrijf:
- prompt: "Geef in het Nederlands: 1) Officiële bedrijfsnaam, 2) Omschrijving in 2-3 zinnen (wat doet het bedrijf, sector, wat maakt het uniek), 3) De sector in één woord"

Als WebFetch faalt (403/timeout), gebruik WebSearch als alternatief:
- query: "[bedrijfsnaam] Nederland bedrijfsprofiel"
- Destilleer bedrijfsnaam, omschrijving en sector uit de zoekresultaten.

Als BEIDE falen, vraag het de gebruiker via AskUserQuestion.

Sla op: BEDRIJFSNAAM, OMSCHRIJVING (2-3 zinnen), SECTOR (één woord), WEBSITE_DOMEIN (bijv. `bol.com`, `coolblue.nl` — zonder https://).

## Stap 3: Lees het AI Panda teambestand

Installeer openpyxl als het nog niet beschikbaar is, en lees het Excel-bestand:

```bash
pip install openpyxl --break-system-packages -q 2>/dev/null
python3 << 'PYEOF'
import openpyxl, json, glob, os

paths = (
    glob.glob("/sessions/*/mnt/*/ai-panda-team.xlsx") +
    glob.glob("/sessions/*/mnt/Ai Panda/ai-panda-team.xlsx") +
    glob.glob(os.path.expanduser("~/Documents/Projecten/Ai Panda Klantpagina/ai-panda-team.xlsx")) +
    glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai-panda-team.xlsx"))
)
if not paths:
    print("ERROR: ai-panda-team.xlsx niet gevonden")
    exit(1)

wb = openpyxl.load_workbook(paths[0])
ws = wb.active
team = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0]:
        team.append({
            "naam": str(row[0]),
            "functie": str(row[1] or ""),
            "team": str(row[2] or ""),
            "foto_url": str(row[3] or ""),
            "email": str(row[5] or "")
        })
print(json.dumps(team, indent=2, ensure_ascii=False))
PYEOF
```

## Stap 4: Laat de gebruiker consultants kiezen

Gebruik AskUserQuestion met multiSelect: true.

BELANGRIJK: maximaal 4 opties per vraag. Verdeel het team over 2 vragen als er meer dan 4 leden zijn:

Vraag 1 (kernteam + leads):
- question: "Welke consultants worden ingezet voor [BEDRIJFSNAAM]? (deel 1/2)"
- header: "Team"
- Toon de eerste 4 teamleden (naam als label, functie als description)

Vraag 2 (overige teamleden):
- question: "Nog meer consultants toevoegen? (deel 2/2 — sla over als je al 3 hebt)"
- header: "Extra"
- Toon de volgende 4 teamleden

Verzamel de geselecteerde namen (streef naar 3 consultants). Match elke geselecteerde naam terug naar het Excel voor functie, foto_url en email.

## Stap 5: Genereer de AI Panda-afbeelding

Gebruik het Python-script in `--client` mode. Dit bouwt automatisch een sector-specifieke prompt, haalt het bedrijfslogo op en geeft het als referentie mee aan Gemini.

### Script uitvoeren

Zoek eerst het script (Cowork-sessie of lokaal):
```bash
SCRIPT=$(find /sessions -name "generate_notion_image.py" 2>/dev/null | head -1)
if [ -z "$SCRIPT" ]; then
  SCRIPT=$(find ~ -maxdepth 6 -name "generate_notion_image.py" 2>/dev/null | head -1)
fi
```

Genereer de afbeelding:
```bash
SAFE_NAME=$(echo "[BEDRIJFSNAAM]" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
cd "$(dirname "$SCRIPT")" && python3 generate_notion_image.py \
  --client \
  --company-name "[BEDRIJFSNAAM]" \
  --sector "[SECTOR]" \
  --logo-domain "[WEBSITE_DOMEIN]" \
  --output "/tmp/panda_${SAFE_NAME}.png" \
  --upload --json
```

De `url` uit de JSON-output is de PANDA_IMAGE_URL voor Stap 6.

### Fallback: Placeholder
Als het script niet gevonden wordt of faalt → gebruik:
`https://ui-avatars.com/api/?name=AI+Panda&size=400&background=000000&color=ffffff&bold=true&format=png`
Meld kort dat een placeholder is gebruikt. GA ALTIJD DOOR.

## Stap 6: Maak de Notion-pagina aan

Gebruik `notion-create-pages`. De `parent` parameter is optioneel: laat weg voor workspace-niveau, of geef een `page_id` mee om de pagina onder een bestaande Notion-pagina aan te maken.

```json
{
  "pages": [{
    "properties": {
      "title": "🏢 [BEDRIJFSNAAM] — AI Panda Klantprofiel"
    },
    "content": "ZIE TEMPLATE"
  }]
}
```

### Notion content template:

```markdown
![AI Panda x [BEDRIJFSNAAM]]([PANDA_IMAGE_URL])

## 🏢 Over [BEDRIJFSNAAM]

[OMSCHRIJVING — 2-3 zinnen van de website/zoekresultaten]

---

## 👥 Jouw AI Panda Team

| | Consultant | Functie | Contact |
|---|---|---|---|
| ![foto]([FOTO_URL_1_OF_AVATAR]) | **[NAAM_1]** | [FUNCTIE_1] | [EMAIL_1] |
| ![foto]([FOTO_URL_2_OF_AVATAR]) | **[NAAM_2]** | [FUNCTIE_2] | [EMAIL_2] |
| ![foto]([FOTO_URL_3_OF_AVATAR]) | **[NAAM_3]** | [FUNCTIE_3] | [EMAIL_3] |

---

## 🗺️ AI Implementatie Roadmap

### 🔍 Fase 1: Discovery (Week 1-2)
> [SPECIFIEK voor dit bedrijf: welke processen worden geanalyseerd, welke AI-kansen zijn relevant voor deze SECTOR]

### 🧪 Fase 2: Pilot (Week 3-6)
> [SPECIFIEK: concrete AI-use case als proof-of-concept, relevant voor hun business]

### 🚀 Fase 3: Implementatie (Week 7-12)
> [SPECIFIEK: uitrol, integratie met systemen die dit type bedrijf gebruikt]

### 📈 Fase 4: Schaling & Optimalisatie (Week 13+)
> [SPECIFIEK: KPIs, uitbreidingsmogelijkheden, relevante metrics voor deze sector]

---

## 📋 Volgende Stappen

- [ ] Kickoff meeting plannen met [BEDRIJFSNAAM]
- [ ] Toegang tot relevante data en systemen regelen
- [ ] Discovery-interviews inplannen met key stakeholders
- [ ] Eerste AI-kansen rapport opleveren

---

*Gegenereerd door AI Panda Cowork — [DATUM in formaat "DD maand YYYY"]*
```

### Invulregels:

**Foto's:** Als Foto-URL in Excel leeg is → gebruik `https://ui-avatars.com/api/?name=[VOORNAAM]&size=150&background=10B981&color=ffffff&bold=true&rounded=true`

**Roadmap:** Maak ELKE fase specifiek. Noem concrete AI-toepassingen per sector:
- Retail/e-commerce → productaanbevelingen, voorraadbeheer, vraagvoorspelling
- Zorg → patiëntmonitoring, planningsoptimalisatie, medische beeldherkenning
- Logistiek → routeoptimalisatie, voorspellend onderhoud, warehouse AI
- Fintech → fraudedetectie, risicobeoordeling, chatbot-automatisering
- Vermijd generieke tekst — dit moet de klant overtuigen.

## Stap 7: Bevestig het resultaat

Toon:
1. ✅ Bevestiging dat de pagina is aangemaakt
2. 🔗 De Notion-URL (klikbaar)
3. 📋 Samenvatting: bedrijfsnaam, gekozen consultants, dat de roadmap is gegenereerd

## Foutafhandeling

De shortcut moet ALTIJD een Notion-pagina opleveren. Geen enkele fout mag de flow stoppen:
- WebFetch faalt → WebSearch → gebruiker vragen
- Image-generatie faalt → placeholder
- Excel niet gevonden → gebruiker vragen om namen
- Notion parent faalt → pagina zonder parent aanmaken
