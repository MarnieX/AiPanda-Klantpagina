# Plan: Nano Banana Pro → Notion (via MCP-connectors)

## Samenvatting

Een volledig geautomatiseerde pipeline om AI-afbeeldingen te genereren en in Notion te plaatsen, opgebouwd uit drie MCP-connectors die al beschikbaar zijn — geen custom code nodig.

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Nano Banana Pro     │     │  Cloudinary          │     │  Notion              │
│  MCP Server          │────▶│  MCP Connector       │────▶│  MCP Connector       │
│                      │     │                      │     │                      │
│  generate_image()    │     │  upload-asset()      │     │  create-pages()      │
│  → base64 + bestand  │     │  → publieke URL      │     │  → pagina met beeld  │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

---

## Benodigdheden

| Wat | Waar | Kosten |
|-----|------|--------|
| Google API Key (Gemini) | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Gratis tier beschikbaar |
| Cloudinary account | [cloudinary.com](https://cloudinary.com/users/register_free) | Gratis (25 credits/maand) |
| Node.js ≥ 18 | Geïnstalleerd in Cowork | Gratis |
| Notion MCP | Al verbonden in Cowork | Gratis |

---

## Stap 1 — Nano Banana Pro MCP-server installeren

### Over de MCP-server

De [`nano-banana-pro-mcp`](https://github.com/mrafaeldie12/nano-banana-pro-mcp) server van mrafaeldie12 biedt:

| Tool | Wat het doet |
|------|-------------|
| `generate_image` | Tekst → afbeelding (Nano Banana Pro, 1K/2K/4K) |
| `edit_image` | Bestaande afbeelding bewerken met prompt |
| `describe_image` | Afbeelding analyseren en beschrijven |

Technische details:
- **Taal:** TypeScript / Node.js
- **NPM package:** `@rafarafarafa/nano-banana-pro-mcp`
- **Transport:** STDIO (standaard MCP integratie)
- **Auth:** Alleen `GEMINI_API_KEY` environment variable
- **Output:** base64 image data + optioneel opslaan als bestand via `outputPath`

### Installatie (één commando)

**Voor Claude Code / Cowork:**
```bash
claude mcp add nano-banana-pro \
  --env GEMINI_API_KEY=jouw-api-key-hier \
  -- npx @rafarafarafa/nano-banana-pro-mcp
```

**Voor Claude Desktop (claude_desktop_config.json):**
```json
{
  "mcpServers": {
    "nano-banana-pro": {
      "command": "npx",
      "args": ["@rafarafarafa/nano-banana-pro-mcp"],
      "env": {
        "GEMINI_API_KEY": "jouw-api-key-hier"
      }
    }
  }
}
```

### Beschikbare modellen

| Model | Code | Kwaliteit | Snelheid |
|-------|------|-----------|----------|
| Nano Banana Pro | `gemini-3-pro-image-preview` | Beste (standaard) | Langzamer |
| Nano Banana Flash | `gemini-2.5-flash-preview-05-20` | Goed | Snel |
| Gemini Flash Exp | `gemini-2.0-flash-exp` | Basis | Snelst |

### Parameters voor generate_image

| Parameter | Type | Opties | Default |
|-----------|------|--------|---------|
| `prompt` | string | Vrije tekst | Verplicht |
| `model` | string | Zie tabel hierboven | `gemini-3-pro-image-preview` |
| `aspectRatio` | string | `1:1`, `3:4`, `4:3`, `9:16`, `16:9` | `1:1` |
| `imageSize` | string | `1K`, `2K`, `4K` | `1K` |
| `images` | array | Base64 referentie-afbeeldingen | Optioneel |
| `outputPath` | string | Bestandspad om op te slaan | Optioneel |

---

## Stap 2 — Cloudinary MCP-connector verbinden

### Waarom Cloudinary?

De Nano Banana Pro MCP retourneert afbeeldingen als **base64 data** of slaat ze op als **lokaal bestand**. Notion heeft een **publieke URL** nodig. Cloudinary lost dit op:

- Beschikbaar als MCP-connector in de Cowork registry
- Gratis tier (25 credits/maand ≈ ~1000 uploads)
- Retourneert een permanente, snelle CDN-URL
- Ondersteunt ook image transformatie (resize, crop, filters)

### Installatie

Verbind de Cloudinary connector vanuit de Cowork connector-instellingen. De connector biedt o.a.:

| Tool | Functie |
|------|---------|
| `upload-asset` | Upload afbeelding → retourneert publieke URL |
| `list-images` | Bekijk geüploade afbeeldingen |
| `download-asset` | Download een asset |

### Alternatief: zonder Cloudinary

Als je geen Cloudinary wilt, zijn er twee alternatieven:

**A. Google Cloud Storage** (als je GCP hebt):
- Upload via `gsutil` of Python SDK
- Maak bestand publiek
- Gebruik de GCS URL in Notion

**B. Imgur** (simpelst, geen account):
- Upload via Imgur API (Client-ID nodig)
- Retourneert publieke URL
- Minder betrouwbaar voor langetermijn

---

## Stap 3 — Notion MCP (al verbonden)

De Notion connector is al actief in je Cowork-sessie en ondersteunt:

| Tool | Gebruik in deze flow |
|------|---------------------|
| `notion-create-pages` | Nieuwe pagina met afbeelding aanmaken |
| `notion-update-page` | Afbeelding toevoegen aan bestaande pagina |
| `notion-search` | Pagina zoeken op titel |
| `notion-fetch` | Bestaande pagina-inhoud ophalen |

Notion toont afbeeldingen via de markdown syntax `![alt](url)` die vertaald wordt naar een extern image block.

---

## De complete flow

### Hoe het werkt (stap voor stap)

```
Gebruiker: "Genereer een afbeelding van een panda die code schrijft
            en zet hem op mijn Notion-pagina 'Blog Posts'"

Claude voert uit:

1. generate_image(
     prompt: "a cute panda writing Python code on a laptop, digital art, vibrant colors",
     aspectRatio: "16:9",
     imageSize: "2K",
     outputPath: "/tmp/panda_coder.png"
   )
   → Retourneert: base64 image data + bestand op /tmp/panda_coder.png

2. upload-asset(
     file: "/tmp/panda_coder.png"
   )
   → Retourneert: https://res.cloudinary.com/xxx/image/upload/v123/panda_coder.png

3. notion-search(query: "Blog Posts")
   → Retourneert: page_id

4. notion-update-page(
     page_id: "...",
     command: "insert_content_after",
     selection_with_ellipsis: "## Laatste sec...",
     new_str: "\n![Panda die code schrijft](https://res.cloudinary.com/xxx/image/upload/v123/panda_coder.png)\n"
   )
   → Afbeelding staat nu in Notion!
```

### Voorbeeld: nieuwe Notion-pagina met afbeelding

```
1. generate_image(prompt: "...", outputPath: "/tmp/image.png")
2. upload-asset(file: "/tmp/image.png") → URL
3. notion-create-pages(
     pages: [{
       properties: { title: "Mijn AI Afbeelding" },
       content: "# Mijn AI Afbeelding\n\n![Beschrijving](URL)\n\n**Prompt:** ...\n**Model:** Nano Banana Pro\n**Resolutie:** 2K"
     }]
   )
```

---

## Setup checklist

### Eenmalige setup (±10 minuten)

- [ ] **Google API Key aanmaken** op [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- [ ] **Nano Banana Pro MCP installeren** via `claude mcp add` of config JSON
- [ ] **Cloudinary account aanmaken** op [cloudinary.com](https://cloudinary.com/users/register_free)
- [ ] **Cloudinary MCP verbinden** vanuit Cowork connector-instellingen
- [ ] **Testen** met een simpele prompt

### Na setup (elke keer)

Gewoon vragen: *"Genereer een afbeelding van X en zet het op mijn Notion-pagina Y"*

---

## Optioneel: Cowork Shortcut

Voor maximaal gemak kun je een shortcut maken die de hele flow automatiseert:

**Naam:** `generate-notion-image`

**Input:** prompt, notion-pagina, aspect ratio, resolutie

**Flow:**
1. Optimaliseer prompt (image-prompt-generator skill)
2. `generate_image` → lokaal bestand
3. `upload-asset` → Cloudinary URL
4. `notion-update-page` → afbeelding in Notion
5. Bevestig aan gebruiker

---

## Kosten samenvatting

| Component | Gratis tier | Betaald |
|-----------|-------------|---------|
| Gemini API (Nano Banana Pro) | ~50 requests/dag gratis | Pay-as-you-go |
| Gemini API (Nano Banana Flash) | Ruimer gratis | Goedkoper |
| Cloudinary | 25 credits/maand (~1000 uploads) | Vanaf $89/maand |
| Notion API | Onbeperkt gratis | - |
| Nano Banana MCP | Open source (MIT) | Gratis |

**Totale kosten voor casual gebruik: €0**

---

## Bronnen

- [nano-banana-pro-mcp (GitHub)](https://github.com/mrafaeldie12/nano-banana-pro-mcp)
- [NPM package](https://www.npmjs.com/package/@rafarafarafa/nano-banana-pro-mcp)
- [Google AI Studio — API Key](https://aistudio.google.com/apikey)
- [Gemini Image Generation docs](https://ai.google.dev/gemini-api/docs/image-generation)
- [Cloudinary MCP connector](https://asset-management.mcp.cloudinary.com)
- [Notion MCP connector](https://mcp.notion.com/mcp)
