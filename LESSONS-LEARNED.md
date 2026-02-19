# Lessons Learned

Gedocumenteerde lessen uit het bouwen en debuggen van de AI Panda Klantpagina plugin, met name rondom Notion markdown rendering en de Cowork omgeving.

---

## Notion Markdown

### 1. Callouts zijn Pandoc-style fenced divs, geen HTML-tags

**Correct:**
```
::: callout {icon="emoji"}
Tekst hier
:::
```

**Fout (wordt stilzwijgend genegeerd):**
```
<callout icon="emoji">tekst</callout>
```

Notion geeft geen foutmelding. De content verdwijnt gewoon. Dit maakt debugging lastig omdat je niet weet waarom een sectie leeg is.

### 2. Column children moeten tab-ingesprongen zijn

**Correct:**
```
<columns>
	<column>
		![](url)
		**Naam**
	</column>
</columns>
```

**Fout (kolommen verschijnen als leeg):**
```
<columns>
	<column>
![](url)
**Naam**
	</column>
</columns>
```

Zonder tab-inspringing (dubbele tab `\t\t` voor content binnen `<column>`) worden de children niet als onderdeel van de kolom herkend. Het resultaat: lege kolommen op de pagina.

### 3. Image captions verschijnen als grijze tekst

`![caption](url)` toont de caption als grijze tekst direct onder de afbeelding. Voor teamfoto's waar de naam al als bold tekst eronder staat, gebruik je `![](url)` (lege caption) om dubbele naamweergave te voorkomen.

### 4. Notion heeft geen embed tag

Er bestaat geen `<embed>` block type in de Notion markdown spec. Het wordt stilzwijgend genegeerd. Gebruik gewone markdown links (`[tekst](url)`) of specifieke mediatags (`<video>`, `<pdf>`, `<audio>`) voor ondersteunde content.

---

## Gemini API

### 5. Modelnamen veranderen zonder waarschuwing

`gemini-2.0-flash-exp` gaf plotseling een 404 terug. Modellen worden regelmatig verwijderd of hernoemd door Google. Standaardmodel is nu `gemini-3-pro-image-preview`.

**Tip:** Beschikbare modellen kun je verifiëren via:
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"
```

### 6. Argparse choices moeten unieke waarden bevatten

Na het updaten van het standaardmodel stond `gemini-3-pro-image-preview` drie keer in de `choices` lijst. Niet schadelijk, maar slordig en verwarrend. Controleer altijd of choices nog kloppen na een model-update.

---

## Cowork Omgeving

### 7. SOCKS proxy vereist httpcore[socks]

In Cowork loopt al het netwerkverkeer via een SOCKS proxy. Python's `httpx` heeft hiervoor `httpcore[socks]` (dat `socksio` installeert) nodig. Zonder deze dependency crasht de MCP server direct bij de eerste API call.

**Oplossing:** Voeg het toe aan de auto-install bootstrap in de MCP server:
```python
subprocess.check_call([sys.executable, "-m", "pip", "install",
    "httpx", "httpcore[socks]", "--break-system-packages", "-q"])
```

### 8. CORS blokkeert browser-uploads naar catbox.moe

Vanuit de Cowork browser-sandbox kun je niet uploaden naar catbox.moe (geen `Access-Control-Allow-Origin` header). De afbeelding wordt wel gegenereerd maar krijgt geen publieke URL.

**Oplossing:** De `upload_image_base64` MCP tool ontvangt base64 data en uploadt server-side via `curl`. Geen CORS omdat de upload niet vanuit de browser gaat.

### 9. catbox.moe is soms onbereikbaar

catbox.moe geeft regelmatig 504 Gateway Timeout errors. Dit is een gratis dienst zonder SLA.

**Oplossing:** Gebruik `0x0.st` als fallback. Beide zijn tijdelijke hostingdiensten (bestanden verlopen). Voor productie zou een permanente hostingoplossing (Cloudinary, S3) beter zijn.

---

## Proces en Werkwijze

### 11. `<video>` tag werkt als embed-workaround voor webapps

Notion heeft geen `<embed>` block type. De `<video>` tag accepteert elke URL en toont hem als embed-block, ook voor non-video content zoals GitHub Pages webapps.

**Correct (werkt als interactieve embed):**
```
<video src="https://marniex.github.io/aipanda-quiz/#data=...">AI-Readiness Quickscan</video>
```

**Fout (stilzwijgend genegeerd):**
```
<embed src="https://..." />
```

Getest met de AI-Readiness Quickscan (GitHub Pages app). De `<video>` tag toont een klikbaar embed-blok dat de webapp laadt. De caption wordt als koptekst boven het blok getoond.

### 12. 0x0.st is betrouwbaarder dan catbox.moe als primaire uploadhost

catbox.moe geeft regelmatig 504 Gateway Timeout terug. 0x0.st is sneller, minder gevoelig voor storingen, en ondersteunt bestanden tot 512 MiB.

**Volgorde in de MCP server:**
1. Probeer 0x0.st (primair, via `curl -F "file=@{path}" https://0x0.st`)
2. Als dat faalt, probeer catbox.moe (fallback)
3. Als beide falen, retourneer lege string en gebruik placeholder

Beide diensten zijn tijdelijk (bestanden verlopen). Notion kopieert afbeeldingen bij aanmaken naar zijn eigen CDN, waardoor verlopen URLs geen probleem zijn voor bestaande pagina's.

---

## Proces en Werkwijze

### 10. Skill templates zijn de bron van waarheid

Als de Notion markdown syntax in het skill template fout is, produceert elke uitvoering dezelfde fout. Het fixen van alleen de output (de gegenereerde Notion-pagina) lost het probleem niet structureel op.

**Aanpak:**
- Fix altijd het template, niet alleen de output
- Voeg een inline syntax-referentie toe aan het template met expliciete "FOUT" voorbeelden
- Dit voorkomt dat dezelfde fouten opnieuw gemaakt worden, ook door andere agents die het template gebruiken
