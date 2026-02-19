# Notion Klantpagina Template — AI Panda

## Notion Markdown Syntax Referentie

Deze syntax is VERPLICHT voor Notion-pagina's. Afwijkingen leiden tot kapotte rendering.

### Afbeeldingen
```
![Caption](URL)
![](URL)              ← zonder caption (geen grijze tekst onder de afbeelding)
```

### Callouts (Pandoc-style fenced divs, NIET HTML-tags)
```
::: callout {icon="emoji"}
Tekst en **rich text** hier
:::
```
FOUT: `<callout icon="emoji">tekst</callout>` — dit werkt NIET.

### Kolommen (children MOETEN met tabs ingesprongen)
```
<columns>
	<column>
		Content hier
	</column>
	<column>
		Content hier
	</column>
</columns>
```
FOUT: children zonder tab-inspringing worden niet gerenderd.

### Tabellen
`<table>` XML, cellen ALLEEN rich text (geen images/blocks).

### To-do's
`- [ ] tekst`

### Dividers
`---`

### Toggle
```
<details>
<summary>Titel</summary>
	Children (ingesprongen)
</details>
```

### Embeds
Notion heeft geen `<embed>` tag. Gebruik:
```
<video src="URL">Caption</video>
```
Werkt ook voor niet-video content zoals webapps.

---

## Template

Paginatitel: `AI Panda x [BEDRIJFSNAAM]`

Hieronder het volledige template. Vervang alle `[VARIABELE]` placeholders met werkelijke waarden.

### Instructies voor dynamische secties
- **Afbeelding:** Als `[PANDA_IMAGE_URL]` leeg is, laat de afbeeldingsregel volledig weg. Stuur nooit een lege `![]()`.
- **Team-kolommen:** Genereer zoveel `<column>` blokken als er geselecteerde consultants zijn. Het template toont 3 als voorbeeld.
- **Foto's:** Als foto_url leeg is, gebruik `https://ui-avatars.com/api/?name=[VOORNAAM]&size=150&background=2EA3F2&color=ffffff&bold=true&rounded=true`
- **Datum:** Formaat "DD maand YYYY" (bijv. "17 februari 2026").
- **Quiz:** De quiz wordt als `<video>` embed getoond (Notion workaround).

---

```markdown
![]([PANDA_IMAGE_URL])

---

::: callout {icon="💬"}
**"[MEDEWERKER_QUOTE]"**
:::

---

<columns>
	<column>
		## Over [BEDRIJFSNAAM]
		[OMSCHRIJVING]
		**Sector:** [SECTOR]
		**Website:** [WEBSITE_DOMEIN]
	</column>
	<column>
		## Over AI Panda
		AI Panda begeleidt organisaties naar AI-volwassenheid. Geen technologie-eerst aanpak, maar mens-eerst: 80% van AI-succes zit in menselijk gedrag, 20% in technologie. Van strategie tot implementatie.
		Wij werken samen met teams op de werkvloer, niet alleen met management. Zo zorgen we dat AI daadwerkelijk landt in de organisatie en niet blijft hangen als een pilot.
		**Tagline:** Making AI Work For You
		**Website:** aipanda.nl
	</column>
</columns>

---

## Jouw AI Panda Team

<columns>
	<column>
		![]([FOTO_URL_1])
		**[NAAM_1]**
		[FUNCTIE_1]
		[TELEFOON_1]
		[EMAIL_1]
	</column>
	<column>
		![]([FOTO_URL_2])
		**[NAAM_2]**
		[FUNCTIE_2]
		[TELEFOON_2]
		[EMAIL_2]
	</column>
	<column>
		![]([FOTO_URL_3])
		**[NAAM_3]**
		[FUNCTIE_3]
		[TELEFOON_3]
		[EMAIL_3]
	</column>
</columns>

*Heb je een vraag? Stuur gerust een berichtje via het emailadres hierboven.*

---

## AI Implementatie Roadmap

Hieronder vind je de roadmap die specifiek is opgesteld voor [BEDRIJFSNAAM] in de [SECTOR]-sector. Elke fase bouwt voort op de vorige.

::: callout {icon="🔍"}
**Fase 1 — Discovery** *(Week 1-2)*

[ROADMAP_FASE_1]
:::

::: callout {icon="🧪"}
**Fase 2 — Pilot** *(Week 3-6)*

[ROADMAP_FASE_2]
:::

::: callout {icon="🚀"}
**Fase 3 — Implementatie** *(Week 7-12)*

[ROADMAP_FASE_3]
:::

::: callout {icon="📈"}
**Fase 4 — Schaling & Optimalisatie** *(Week 13+)*

[ROADMAP_FASE_4]
:::

---

## AI-Readiness Quickscan

Ontdek in 2 minuten hoe ver [BEDRIJFSNAAM] staat met AI. Beantwoord 5 korte vragen en krijg direct je profiel.

<video src="[QUIZ_URL]">AI-Readiness Quickscan</video>

---

*Gegenereerd door AI Panda Cowork — [DATUM]*
```
