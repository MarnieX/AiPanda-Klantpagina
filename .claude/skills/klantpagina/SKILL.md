---
name: klantpagina
description: "Genereer een professionele Notion-klantpagina voor AI Panda. Haalt bedrijfsinfo op van de website, leest consultants uit een Excel, genereert een AI Panda-afbeelding en maakt een complete Notion-pagina met roadmap."
---

# AI Panda Klantpagina Generator

Je genereert een professionele Notion-klantpagina voor AI Panda. Volg de stappen exact in volgorde. Start parallelstappen altijd tegelijk om snelheid te winnen.

Gebruik TodoWrite om voortgang te tonen:
1. Klant en consultants ophalen
2. Bedrijfsinfo + Excel matchen (parallel)
3. Bevestiging vragen
4. Afbeelding genereren + content voorbereiden (parallel)
5. Image uploaden
6. Notion-pagina aanmaken
7. Resultaat bevestigen

---

## Stap 1: Vraag om bedrijf

Gebruik AskUserQuestion:
- question: "Voor welk bedrijf maak je een klantpagina? Geef de naam of website-URL."
- header: "Klant"
- options: exact drie voorbeelden: "Coolblue", "bol.com", "Jumbo" — gebruik GEEN optie als "Ander bedrijf". De gebruiker typt het eigen bedrijf via het "Other"-tekstveld.
- multiSelect: false

Sla op: KLANT_INPUT (naam of URL zoals ingetypt door gebruiker)

---

## Stap 2: Vraag om consultants

Gebruik AskUserQuestion:
- question: "Welke consultants werken aan dit traject? Typ de namen (gescheiden door komma's)."
- header: "Consultants"
- options: drie voorbeeldantwoorden zoals "Marnix, Noud, Rick", "Ik typ ze zelf", "Alleen Marnix" — de gebruiker typt via "Other" de juiste namen
- multiSelect: false

Sla op: CONSULTANT_INPUT (ruwe tekst, bijv. "Marnix, Lisa")

---

## Stap 3: Parallel ophalen (start beide tegelijk)

### 3A — Bedrijfsinfo ophalen

Als KLANT_INPUT een URL bevat (http of een domein), gebruik WebFetch direct op die URL.
Anders, bouw de URL op als `https://www.[klant].nl` of zoek via WebSearch.

WebFetch prompt: "Geef in het Nederlands: 1) Officiële bedrijfsnaam, 2) Omschrijving in 2-3 zinnen (wat doet het bedrijf, sector, wat maakt het uniek), 3) De sector in één woord"

Fallback: als WebFetch faalt (403/timeout) → WebSearch met query "[klant] Nederland bedrijfsprofiel"
Fallback 2: als beide falen → gebruik de naam zoals ingetypt, omschrijving leeg laten voor bevestigingsstap

Sla op: BEDRIJFSNAAM, OMSCHRIJVING, SECTOR, WEBSITE_DOMEIN (bijv. `bol.com`, zonder https://)

### 3B — Excel lezen en namen matchen

```bash
pip install openpyxl --break-system-packages -q 2>/dev/null
python3 << 'PYEOF'
import openpyxl, json, glob, os, sys

paths = (
    glob.glob("/sessions/*/mnt/*/data/ai-panda-team.xlsx") +
    glob.glob("/sessions/*/mnt/*/ai-panda-team.xlsx") +
    glob.glob("/sessions/*/mnt/Ai Panda/data/ai-panda-team.xlsx") +
    glob.glob("/sessions/*/mnt/Ai Panda/ai-panda-team.xlsx") +
    glob.glob(os.path.expanduser("~/Documents/Projecten/Ai Panda Klantpagina/data/ai-panda-team.xlsx")) +
    glob.glob(os.path.expanduser("~/Documents/Projecten/Ai Panda Klantpagina/ai-panda-team.xlsx")) +
    glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ai-panda-team.xlsx")) +
    glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai-panda-team.xlsx"))
)
if not paths:
    print(json.dumps({"error": "ai-panda-team.xlsx niet gevonden"}))
    sys.exit(0)

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

Match de getypte namen uit CONSULTANT_INPUT aan teamleden (case-insensitief, gedeeltelijke match is ok).
Sla op: CONSULTANTS (lijst met naam, functie, foto_url, email per consultant)

Fallback als Excel niet gevonden: gebruik de namen zoals ingetypt, functie/email leeg. GA ALTIJD DOOR.

---

## Stap 4: Bevestigingsscherm

Toon de opgehaalde informatie overzichtelijk aan de gebruiker:

```
📋 Samenvatting — klopt dit?

🏢 Bedrijf: [BEDRIJFSNAAM]
🌐 Website: [WEBSITE_DOMEIN]
📝 Sector: [SECTOR]

Over het bedrijf:
[OMSCHRIJVING]

👥 Consultants:
• [NAAM_1] — [FUNCTIE_1]
• [NAAM_2] — [FUNCTIE_2]
• [NAAM_3] — [FUNCTIE_3]
```

Gebruik daarna AskUserQuestion:
- question: "Klopt bovenstaande informatie, of wil je iets aanpassen?"
- header: "Bevestiging"
- options:
  - "Ziet er goed uit, ga door" (Recommended)
  - "Bedrijfsinfo aanpassen"
  - "Consultants aanpassen"

Als de gebruiker wil aanpassen: vraag wat er anders moet en verwerk de correctie. Herhaal het bevestigingsscherm daarna niet opnieuw — vertrouw op de aanpassing en ga door.

---

## Stap 5: Parallel uitvoeren (start beide tegelijk na bevestiging)

### 5A — AI Panda-afbeelding genereren

Zoek het script:
```bash
SCRIPT=$(find /sessions -name "generate_notion_image.py" 2>/dev/null | head -1)
if [ -z "$SCRIPT" ]; then
  SCRIPT=$(find ~ -maxdepth 6 -name "generate_notion_image.py" 2>/dev/null | head -1)
fi
echo "$SCRIPT"
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

De `url` uit de JSON-output is PANDA_IMAGE_URL.

Fallback: gebruik `https://ui-avatars.com/api/?name=AI+Panda&size=400&background=000000&color=ffffff&bold=true&format=png` en meld dit kort. GA ALTIJD DOOR.

### 5B — Roadmap content voorbereiden

Bereid de sector-specifieke roadmap voor (geen externe call nodig, kan meteen):

Maak elke fase specifiek voor SECTOR en BEDRIJFSNAAM. Vermijd generieke tekst. Voorbeelden per sector:
- Retail/e-commerce → productaanbevelingen, voorraadbeheer, vraagvoorspelling
- Zorg → patiëntmonitoring, planningsoptimalisatie, medische beeldherkenning
- Logistiek → routeoptimalisatie, voorspellend onderhoud, warehouse-automatisering
- Fintech → fraudedetectie, risicobeoordeling, chatbot-automatisering
- B2B/dienstverlening → offerteautomatisering, kennismanagement, CRM-verrijking

Sla op als ROADMAP_CONTENT (markdown tekst voor fase 1 t/m 4).

---

## Stap 6: Notion-pagina aanmaken

Wacht tot zowel 5A als 5B klaar zijn. Gebruik dan `notion-create-pages`.

De `parent` parameter is optioneel: laat weg voor workspace-niveau, of geef een `page_id` mee als je de pagina onder een bestaande pagina wilt plaatsen.

**Foto's:** Als foto_url leeg is → gebruik `https://ui-avatars.com/api/?name=[VOORNAAM]&size=150&background=10B981&color=ffffff&bold=true&rounded=true`

**Datum:** Gebruik formaat "DD maand YYYY" (bijv. "17 februari 2026").

### Content template (simpele versie — definitief template volgt later):

```markdown
![AI Panda x [BEDRIJFSNAAM]]([PANDA_IMAGE_URL])

## 🏢 Over [BEDRIJFSNAAM]

[OMSCHRIJVING]

**Sector:** [SECTOR] | **Website:** [WEBSITE_DOMEIN]

---

## 👥 Jouw AI Panda Team

| | Consultant | Functie | Contact |
|---|---|---|---|
| ![foto]([FOTO_URL_1]) | **[NAAM_1]** | [FUNCTIE_1] | [EMAIL_1] |
| ![foto]([FOTO_URL_2]) | **[NAAM_2]** | [FUNCTIE_2] | [EMAIL_2] |
| ![foto]([FOTO_URL_3]) | **[NAAM_3]** | [FUNCTIE_3] | [EMAIL_3] |

---

## 🗺️ AI Implementatie Roadmap

### 🔍 Fase 1: Discovery (Week 1-2)
[ROADMAP_FASE_1]

### 🧪 Fase 2: Pilot (Week 3-6)
[ROADMAP_FASE_2]

### 🚀 Fase 3: Implementatie (Week 7-12)
[ROADMAP_FASE_3]

### 📈 Fase 4: Schaling & Optimalisatie (Week 13+)
[ROADMAP_FASE_4]

---

## 📋 Volgende Stappen

- [ ] Kickoff meeting plannen met [BEDRIJFSNAAM]
- [ ] Toegang tot relevante data en systemen regelen
- [ ] Discovery-interviews inplannen met key stakeholders
- [ ] Eerste AI-kansen rapport opleveren

---

## 🤖 Over AI Panda Cowork

*Meer weten over het platform waarmee dit traject wordt begeleid? Een volledige uitleg volgt binnenkort op een aparte pagina.*

---

*Gegenereerd door AI Panda Cowork — [DATUM]*
```

---

## Stap 7: Bevestig het resultaat

Toon:
1. ✅ Notion-pagina aangemaakt
2. 🔗 De Notion-URL (klikbaar)
3. 📋 Korte samenvatting: bedrijf, consultants, roadmap gegenereerd

---

## Foutafhandeling

De skill moet ALTIJD een Notion-pagina opleveren. Geen enkele fout mag de flow stoppen:
- WebFetch faalt → WebSearch → gebruiker vragen
- Excel niet gevonden → namen gebruiken zoals ingetypt
- Image-generatie faalt → placeholder URL, doorgaan
- Notion parent faalt → pagina zonder parent aanmaken
