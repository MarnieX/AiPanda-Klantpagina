# Workflow: Nano Banana Pro (Google) naar Notion — zonder Higgsfield

## Overzicht

Deze workflow beschrijft hoe je vanuit Claude Cowork afbeeldingen genereert met **Nano Banana Pro** (Google Gemini 3 Pro Image) via een Google API key, en deze direct in een Notion-pagina plaatst. Geen Higgsfield account nodig.

---

## Wat je nodig hebt

| Onderdeel | Waar te krijgen | Kosten |
|-----------|----------------|--------|
| Google API Key | [aistudio.google.com](https://aistudio.google.com) | Gratis tier beschikbaar |
| Notion MCP-connector | Al verbonden in Cowork | Gratis |
| Image hosting (voor Notion) | Zie Stap 3 | Gratis opties beschikbaar |

---

## Het probleem: afbeelding naar Notion

De Gemini API retourneert afbeeldingen als **inline base64 data** (niet als URL). Notion vereist een **publiek toegankelijke URL** om een afbeelding te tonen. Er is dus een tussenstap nodig: de gegenereerde afbeelding moet ergens gehost worden.

---

## Stap 1 — Google API Key instellen

1. Ga naar [Google AI Studio](https://aistudio.google.com)
2. Klik op "Get API Key" → "Create API Key"
3. Bewaar de key veilig

Stel de key in als environment variable:

```bash
export GEMINI_API_KEY="jouw-api-key-hier"
```

---

## Stap 2 — Afbeelding genereren met Nano Banana Pro

### Installatie

```bash
pip install -U google-genai Pillow
```

### Python code

```python
from google import genai
from google.genai import types

client = genai.Client()  # Pakt GEMINI_API_KEY automatisch op

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",    # Nano Banana Pro
    contents=["Een fotorealistische afbeelding van een berglandschap bij zonsopgang"],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"          # Opties: 1K, 2K, 4K
        ),
    ),
)

# Sla de afbeelding op
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
        print("Afbeelding opgeslagen!")
    elif part.text is not None:
        print(f"Model tekst: {part.text}")
```

### Beschikbare modellen

| Model | Code | Snelheid | Kwaliteit |
|-------|------|----------|-----------|
| Nano Banana (Flash) | `gemini-2.5-flash-image` | Snel | Goed |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Langzamer | Beste |

### Parameters

| Parameter | Opties | Default |
|-----------|--------|---------|
| image_size | "1K", "2K", "4K" | "1K" |
| aspect_ratio | "1:1", "3:4", "4:3", "9:16", "16:9" | model kiest |
| response_modalities | Altijd `["TEXT", "IMAGE"]` | Verplicht |

---

## Stap 3 — Afbeelding hosten (nodig voor Notion)

Notion kan alleen afbeeldingen tonen via een externe URL. Hier zijn de opties om je gegenereerde afbeelding publiek beschikbaar te maken:

### Optie A: Cloudinary (aanbevolen — gratis tier, betrouwbaar)

```python
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="jouw-cloud-name",
    api_key="jouw-cloudinary-key",
    api_secret="jouw-cloudinary-secret"
)

result = cloudinary.uploader.upload("generated_image.png")
image_url = result["secure_url"]
# → https://res.cloudinary.com/jouw-cloud/image/upload/v123/abc.png
```

Gratis tier: 25 credits/maand (voldoende voor ~1000 uploads).

### Optie B: Google Cloud Storage (als je GCP hebt)

```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket("jouw-bucket-naam")
blob = bucket.blob("generated/afbeelding.png")
blob.upload_from_filename("generated_image.png")
blob.make_public()
image_url = blob.public_url
# → https://storage.googleapis.com/jouw-bucket/generated/afbeelding.png
```

### Optie C: Imgur (simpelst, geen account nodig)

```python
import requests, base64

with open("generated_image.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    "https://api.imgur.com/3/image",
    headers={"Authorization": "Client-ID JOUW_IMGUR_CLIENT_ID"},
    data={"image": image_data}
)
image_url = response.json()["data"]["link"]
# → https://i.imgur.com/abc123.png
```

### Optie D: Directe base64 in Notion (experimenteel)

Notion ondersteunt officieel geen base64 data URIs in image blocks. Deze optie werkt dus **niet** betrouwbaar.

---

## Stap 4 — Afbeelding in Notion plaatsen

Met de image URL uit stap 3 gebruik je de Notion MCP-connector in Cowork.

### Nieuwe pagina aanmaken

Via `notion-create-pages`:

```markdown
# Berglandschap bij zonsopgang

![Gegenereerd met Nano Banana Pro](https://res.cloudinary.com/jouw-cloud/image/upload/abc.png)

**Prompt:** "Een fotorealistische afbeelding van een berglandschap bij zonsopgang"
**Model:** Nano Banana Pro (gemini-3-pro-image-preview)
**Resolutie:** 2K, 16:9
```

### Toevoegen aan bestaande pagina

Via `notion-update-page` met `insert_content_after`:

```json
{
    "command": "insert_content_after",
    "selection_with_ellipsis": "## Laatste sec...",
    "new_str": "\n![Gegenereerde afbeelding](https://image-url-hier.png)\n"
}
```

---

## Volledige automatische flow

### Als Python-script (handmatig uitvoeren)

```python
"""
Nano Banana Pro → Notion pipeline
Genereert een afbeelding en plaatst deze in Notion
"""
from google import genai
from google.genai import types
import cloudinary, cloudinary.uploader
import os

# 1. Configuratie
client = genai.Client()
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# 2. Genereer afbeelding
prompt = "Een futuristische stad bij zonsondergang, fotorealistisch, 8k detail"
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(image_size="2K", aspect_ratio="16:9"),
    ),
)

# 3. Sla op en upload
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("/tmp/generated.png")
        result = cloudinary.uploader.upload("/tmp/generated.png")
        image_url = result["secure_url"]
        print(f"Image URL: {image_url}")
        break

# 4. Notion-stap → voer uit via Cowork Notion MCP
print(f"Klaar! Gebruik deze URL in Notion: {image_url}")
```

### Als MCP-server (aanbevolen voor hergebruik)

De krachtigste aanpak is een **eigen MCP-server** bouwen die Nano Banana Pro wrapt. Dan kan Claude de tool direct aanroepen vanuit elk gesprek.

**Tools die de MCP-server zou bieden:**

| Tool | Functie |
|------|---------|
| `generate_image` | Tekst → afbeelding via Nano Banana Pro |
| `edit_image` | Bestaande afbeelding bewerken met prompt |
| `upload_to_host` | Afbeelding uploaden naar Cloudinary/GCS |
| `generate_and_host` | Alles-in-één: genereer + upload + retourneer URL |

**Voorbeeld aanroep vanuit Cowork:**

```
Gebruiker: "Maak een afbeelding van een panda die code schrijft en zet hem op mijn Notion-pagina"

Claude:
  1. generate_and_host(prompt="een schattige panda die Python code schrijft op een laptop, digital art")
     → retourneert https://res.cloudinary.com/.../panda_coder.png
  2. notion-update-page(page_id="...", insert image met URL)
  3. Klaar!
```

### Als Cowork Shortcut (meest gebruiksvriendelijk)

Een shortcut combineert alles in één herhaalbaar commando:

**Trigger:** `/generate-notion-image`

**Parameters:**
- `prompt` — beschrijving van de gewenste afbeelding
- `notion_page` — URL of naam van de Notion-pagina
- `quality` — 1K / 2K / 4K (default: 2K)

**Flow:**
1. Optimaliseer prompt (image-prompt-generator skill)
2. Genereer afbeelding via Gemini API
3. Upload naar image host
4. Voeg toe aan Notion-pagina
5. Bevestig aan gebruiker met preview

---

## Kosten overzicht

| Component | Gratis tier | Betaald |
|-----------|-------------|---------|
| Gemini API (Nano Banana Pro) | Beperkt gratis gebruik | Pay-as-you-go |
| Gemini API (Nano Banana Flash) | Ruimer gratis gebruik | Goedkoper dan Pro |
| Cloudinary | 25 credits/maand | Vanaf $89/maand |
| Imgur | Gratis (rate limited) | - |
| Google Cloud Storage | $0.02/GB/maand | Pay-as-you-go |
| Notion API | Gratis | - |

---

## Vergelijking: Direct Google vs. via Higgsfield

| Aspect | Direct Google API | Via Higgsfield |
|--------|------------------|----------------|
| Modellen | Nano Banana + Nano Banana Pro | 100+ modellen (incl. Nano Banana Pro, FLUX, etc.) |
| Authenticatie | Google API Key | Higgsfield API Key + Secret |
| Image output | Base64 (upload nodig) | Directe URL (7 dagen geldig) |
| Extra setup | Image hosting nodig | Geen extra hosting nodig |
| Kosten | Google pricing | Higgsfield credits (~$0.05/image) |
| MCP-server | Zelf bouwen | Community server beschikbaar |
| Snelheid | Synchroon (direct resultaat) | Asynchroon (polling nodig) |
| Video generatie | Nee | Ja (DoP model) |

**Voordeel van direct Google:** Geen tussenpersoon, synchrone API (direct resultaat), goedkoper bij hoog volume.

**Voordeel van Higgsfield:** Kant-en-klare MCP-server, directe URLs (geen hosting nodig), toegang tot 100+ modellen.

---

## Aanbevolen aanpak

**Snelste start:** Bouw een simpel Python-script (stap 2 + 3) dat je vanuit Cowork kunt uitvoeren. Gebruik Cloudinary als image host.

**Meest schaalbaar:** Bouw een eigen MCP-server met de `mcp-builder` skill in Cowork. Dan is de flow volledig geautomatiseerd.

**Volgende stappen:**
1. Maak een API key aan op [aistudio.google.com](https://aistudio.google.com)
2. Kies een image hosting optie (Cloudinary aanbevolen)
3. Laat Claude de MCP-server of het script bouwen
4. Test met een eerste afbeelding naar Notion
