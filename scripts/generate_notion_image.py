#!/usr/bin/env python3
"""
Nano Banana Pro → Notion Pipeline
==================================
Genereert een afbeelding via Google Gemini API,
upload naar een image host, en retourneert de URL.

Gebruik:
  python generate_notion_image.py "een panda die code schrijft"
  python generate_notion_image.py "berglandschap bij zonsopgang" --ratio 16:9 --size 2K
  python generate_notion_image.py --client --company-name "KPN" --sector telecom --brand-colors "#00A83E,#FFFFFF" --logo-domain kpn.com

Vereisten:
  pip install google-genai Pillow python-dotenv requests opencv-python-headless ddgs

Configuratie:
  .env bestand met GEMINI_API_KEY=jouw-key
"""
import os
import sys
import argparse
import base64
import json
import tempfile
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types


def load_api_key():
    """Laad API key uit environment of .env fallback.

    In Cowork/CLI wordt de key gezet via ~/.claude/settings.json.
    Fallback: .env in projectroot (lokale ontwikkeling).
    """
    key = os.getenv("GEMINI_API_KEY")
    if key:
        print("[ENV] GEMINI_API_KEY geladen uit environment")
        return key

    # Fallback: .env in projectroot of working directory
    for p in [Path(__file__).parent.parent / ".env", Path(".env")]:
        if p.exists():
            load_dotenv(p)
            key = os.getenv("GEMINI_API_KEY")
            if key:
                print(f"[ENV] GEMINI_API_KEY geladen uit {p}")
                return key

    print("ERROR: GEMINI_API_KEY niet gevonden. Zie README.md voor configuratie.")
    sys.exit(1)


SECTOR_BACKGROUNDS = {
    "telecom": "a modern telecom operations center with fiber optic cables, network equipment visible through glass walls, and digital displays showing connectivity maps",
    "retail": "a bright, modern retail headquarters with product displays visible in the background, shopping analytics on screens, and a vibrant commercial atmosphere",
    "e-commerce": "a modern e-commerce fulfillment center with package conveyors visible through windows, real-time order dashboards on screens, and a fast-paced digital commerce atmosphere",
    "finance": "a sleek financial trading floor with market data screens, modern glass architecture, and a sophisticated corporate atmosphere",
    "zorg": "a modern healthcare innovation lab with medical technology, patient care dashboards on screens, and a clean clinical-yet-warm atmosphere",
    "logistiek": "a high-tech logistics control room with route optimization maps, warehouse robotics visible through windows, and real-time tracking dashboards",
    "tech": "a cutting-edge tech campus with open workspaces, code on large screens, and a creative Silicon Valley atmosphere",
    "onderwijs": "a modern educational innovation space with interactive whiteboards, learning analytics on screens, and a bright collaborative atmosphere",
    "energie": "a sustainable energy control center with solar and wind farm monitoring dashboards, green technology displays, and an eco-modern atmosphere",
    "overheid": "a modern government innovation hub with civic data dashboards, smart city visualizations on screens, and a transparent collaborative atmosphere",
    "food": "a modern food production facility with industrial bakery equipment, recipe management screens, and warm lighting from fresh-baked goods",
    "horeca": "a modern food production facility with industrial bakery equipment, recipe management screens, and warm lighting from fresh-baked goods",
    "bakkerij": "a modern artisan bakery headquarters with fresh bread displays, production planning dashboards, warm golden lighting, and the smell of fresh-baked goods in the air",
}


def build_client_prompt(company_name, sector=None, brand_colors=None, has_logo=False):
    """Bouw een rijke klantspecifieke prompt voor AI Panda samenwerking."""
    # Sector-specifieke achtergrond
    sector_key = (sector or "tech").lower()
    background = SECTOR_BACKGROUNDS.get(sector_key, SECTOR_BACKGROUNDS["tech"])

    # Brandkleuren verwerken
    color_instruction = ""
    if brand_colors:
        colors = [c.strip() for c in brand_colors.split(",")]
        color_names = ", ".join(colors)
        color_instruction = (
            f" The room features accent colors matching the company brand: {color_names} "
            f"in wall panels, furniture details, and ambient lighting."
        )

    # Logo instructie
    logo_instruction = ""
    if has_logo:
        logo_instruction = (
            " The company logo (provided as reference image) appears naturally integrated "
            "in the scene: clearly visible on a large screen or monitor in the background, "
            "and subtly on a coffee mug or notebook on the table. "
            "The logo must be rendered accurately and recognizably, not altered or distorted."
        )

    prompt = (
        f"A photorealistic, cinematic scene of an AI Panda consulting session at {company_name}. "
        f"The panda character must closely match the reference image provided: "
        f"a realistic anthropomorphic giant panda with black-and-white fur, round ears, "
        f"black eye patches, wearing a sharp dark business suit. Same character style, "
        f"same realistic fur texture and proportions. Different pose and scene is fine. "
        f"The panda is leading an energetic whiteboard brainstorming session with a diverse team of 3 human "
        f"colleagues seated around a conference table. The panda is standing, gesturing enthusiastically "
        f"at the whiteboard which shows AI automation concepts, workflow diagrams, and the text "
        f"'{company_name}' written prominently. "
        f"The 3 human colleagues have a West-European appearance — a natural mix of men and women, "
        f"ranging in age from mid-20s to early 40s. They are diverse within a Western-European context: "
        f"varied hair colours (blond, brown, dark), different facial features, "
        f"some with glasses, dressed in modern smart-casual business attire. "
        f"The setting is {background}.{color_instruction}{logo_instruction} "
        f"Professional photography style, warm golden hour lighting, shallow depth of field, "
        f"collaborative energy, team looks engaged and inspired. "
        f"High detail, photorealistic, 8K quality."
    )

    return prompt


def generate_image(prompt, model="gemini-3-pro-image-preview", aspect_ratio="1:1",
                   image_size="2K", reference_images=None):
    """Genereer afbeelding via Gemini API, optioneel met referentie-images."""
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    ref_count = len(reference_images) if reference_images else 0
    print(f"Model:        {model}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"Image size:   {image_size}")
    if ref_count:
        print(f"Ref images:   {ref_count}")
    print(f"Prompt:       {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print("Generating...")

    # Bouw config
    config_kwargs = {
        "response_modalities": ["TEXT", "IMAGE"],
    }

    # Image config alleen voor image-specifieke modellen
    if "image" in model or "imagen" in model:
        config_kwargs["image_config"] = types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        )

    # Bouw contents: prompt + optioneel referentie-images
    contents = [prompt]
    if reference_images:
        contents.extend(reference_images)

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    # Verwerk response
    image_data = None
    description = None

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part
        elif part.text is not None:
            description = part.text

    if not image_data:
        print("ERROR: Geen afbeelding gegenereerd")
        sys.exit(1)

    return image_data, description


def save_image(image_part, output_path):
    """Sla afbeelding op als bestand."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    image = image_part.as_image()
    image.save(output_path)
    size = os.path.getsize(output_path)
    print(f"Opgeslagen:   {output_path} ({size:,} bytes)")
    return output_path


MIN_LOGO_SIZE = 48  # minimum pixels breed/hoog om als echt logo te accepteren


def _load_image_from_url(url, label=""):
    """Download een afbeelding van een URL en retourneer een PIL Image, of None."""
    import requests
    from PIL import Image
    import io

    try:
        resp = requests.get(url, timeout=10,
                            headers={"User-Agent": "Mozilla/5.0 (compatible; AI-Panda-Bot/1.0)"})
        resp.raise_for_status()
        if len(resp.content) < 200:
            return None
        img = Image.open(io.BytesIO(resp.content))
        if img.size[0] < MIN_LOGO_SIZE or img.size[1] < MIN_LOGO_SIZE:
            return None
        if label:
            print(f"  Logo gevonden via {label}: {img.size[0]}x{img.size[1]} px")
        return img
    except Exception:
        return None


def _try_google_favicon(domain):
    """Stap 1: Google Favicons API."""
    url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
    return _load_image_from_url(url, "Google Favicons")


def _try_website_scrape(domain):
    """Stap 2: Scrape og:image of apple-touch-icon van de website."""
    import requests
    import re

    for scheme in ["https", "http"]:
        try:
            resp = requests.get(
                f"{scheme}://www.{domain}",
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0 (compatible; AI-Panda-Bot/1.0)"},
                allow_redirects=True,
            )
            html = resp.text

            # og:image heeft vaak een goed logo
            patterns = [
                r'og:image["\s]+content=["\']([^"\']+)',
                r'content=["\']([^"\']+)["\'][^>]+og:image',
                r'apple-touch-icon[^>]+href=["\']([^"\']+)',
                r'href=["\']([^"\']+)["\'][^>]+apple-touch-icon',
                r'<img[^>]+(?:class|id)=["\'][^"\']*logo[^"\']*["\'][^>]+src=["\']([^"\']+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    logo_url = match.group(1)
                    if logo_url.startswith("//"):
                        logo_url = f"{scheme}:{logo_url}"
                    elif logo_url.startswith("/"):
                        logo_url = f"{scheme}://www.{domain}{logo_url}"
                    img = _load_image_from_url(logo_url, "website scrape")
                    if img:
                        return img
        except Exception:
            continue
    return None


def _try_duckduckgo_favicon(domain):
    """Stap 3: DuckDuckGo favicon API."""
    url = f"https://icons.duckduckgo.com/ip3/{domain}.ico"
    return _load_image_from_url(url, "DuckDuckGo favicon")


def _try_image_search(company_name, domain=None):
    """Stap 4: DuckDuckGo afbeeldingen zoeken naar het logo."""
    try:
        from ddgs import DDGS
    except ImportError:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            print("  WARNING: ddgs package niet geinstalleerd (pip install ddgs)")
            return None

    queries = [
        f"{company_name} logo PNG transparent",
        f"{company_name} logo",
        f"{company_name} beeldmerk",
    ]
    if domain:
        queries.insert(0, f"{company_name} site:{domain} logo")

    print(f"  Logo zoeken via DuckDuckGo afbeeldingen...")
    for query in queries:
        try:
            results = list(DDGS().images(query, max_results=15))
            for r in results:
                img_url = r.get("image", "")
                if not img_url:
                    continue
                img = _load_image_from_url(img_url, f"DuckDuckGo '{query[:40]}'")
                if img:
                    return img
        except Exception as e:
            print(f"  Zoekopdracht mislukt ({query[:40]}...): {e}")
            continue

    return None


def resolve_logo(company_name, domain=None):
    """Zoek het bedrijfslogo via een fallback-keten van vier stappen.

    Returns: tuple (tmp_file_path, pil_image) of (None, None) als niets werkt.
    """
    from PIL import Image

    label = domain or company_name
    print(f"Logo zoeken voor {label}...")

    steps = []
    if domain:
        steps.append(("Google Favicons",    lambda: _try_google_favicon(domain)))
        steps.append(("Website scrape",     lambda: _try_website_scrape(domain)))
        steps.append(("DuckDuckGo favicon", lambda: _try_duckduckgo_favicon(domain)))
    steps.append(("DuckDuckGo image search", lambda: _try_image_search(company_name, domain)))

    logo_img = None
    for step_name, step_fn in steps:
        print(f"  Probeer: {step_name}...")
        try:
            result = step_fn()
            if result is not None:
                logo_img = result
                break
        except Exception as e:
            print(f"  {step_name} mislukt: {e}")
            continue

    if logo_img is None:
        print(f"WARNING: Geen bruikbaar logo gevonden voor {label}, afbeelding wordt zonder logo gegenereerd.")
        return None, None

    # Sla op als tijdelijk bestand voor legacy compositing
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    logo_img.save(tmp.name)
    tmp.close()
    return tmp.name, logo_img


def detect_badge(image_path):
    """Detecteer witte badge op het jasje van de panda via OpenCV."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("WARNING: opencv-python-headless niet geinstalleerd. Badge detectie overgeslagen.")
        print("  Installeer met: pip install opencv-python-headless")
        return None

    print("Badge detecteren...")
    img = cv2.imread(image_path)
    if img is None:
        print("WARNING: Kon afbeelding niet laden voor badge detectie")
        return None

    height, width = img.shape[:2]
    image_area = height * width

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Filter op wit/lichtgrijs (de badge)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 40, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Morphologische operaties om gaten te dichten
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_badge = None
    best_score = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        area_ratio = area / image_area

        # Filter op grootte
        if area_ratio < 0.01 or area_ratio > 0.10:
            continue

        # Filter op aspect ratio (roughly vierkant)
        aspect = w / h if h > 0 else 0
        if aspect < 0.5 or aspect > 2.0:
            continue

        # Filter op positie: borstgebied (onder het gezicht)
        center_y = (y + h / 2) / height
        center_x = (x + w / 2) / width
        if center_y < 0.38 or center_y > 0.78:
            continue
        if center_x < 0.20 or center_x > 0.80:
            continue

        # Solidity check: badge should be compact (filled vs bounding box)
        contour_area = cv2.contourArea(contour)
        solidity = contour_area / area if area > 0 else 0
        if solidity < 0.4:
            continue

        # Score: prefer groter, more compact, and more central
        score = area_ratio * solidity * (1.0 - abs(center_x - 0.5))
        if score > best_score:
            best_score = score
            best_badge = (x, y, w, h)

    if best_badge:
        x, y, w, h = best_badge
        print(f"Badge gevonden: x={x}, y={y}, w={w}, h={h}")
    else:
        print("WARNING: Geen badge gedetecteerd in de afbeelding")

    return best_badge


def composite_logo(image_path, logo_path, badge_rect, output_path):
    """Plaats bedrijfslogo over de gedetecteerde badge."""
    from PIL import Image

    print("Logo compositen over badge...")

    try:
        panda_img = Image.open(image_path).convert("RGBA")
        logo_img = Image.open(logo_path).convert("RGBA")

        x, y, w, h = badge_rect

        # Resize logo naar 80% van badge-grootte (wat padding)
        logo_w = int(w * 0.8)
        logo_h = int(h * 0.8)
        logo_img = logo_img.resize((logo_w, logo_h), Image.LANCZOS)

        # Centreer logo binnen de badge bounding box
        paste_x = x + (w - logo_w) // 2
        paste_y = y + (h - logo_h) // 2

        # Paste met alpha-masker
        panda_img.paste(logo_img, (paste_x, paste_y), logo_img)

        # Sla op als RGB (PNG zonder alpha voor compatibiliteit)
        panda_img.convert("RGB").save(output_path)
        print(f"Gecomposite afbeelding opgeslagen: {output_path}")
        return output_path
    except Exception as e:
        print(f"WARNING: Compositing mislukt: {e}")
        return None


def upload_to_cloudinary(filepath):
    """Upload afbeelding naar Cloudinary (persistent hosting)."""
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        print("Cloudinary niet geconfigureerd, fallback naar catbox.moe...")
        return upload_to_catbox(filepath)

    try:
        import cloudinary
        import cloudinary.uploader

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
        )
        print("Uploading naar Cloudinary...")
        result = cloudinary.uploader.upload(filepath, folder="ai-panda")
        url = result["secure_url"]
        print(f"URL:          {url}")
        return url
    except ImportError:
        print("Cloudinary package niet gevonden, fallback naar catbox.moe...")
        return upload_to_catbox(filepath)
    except Exception as e:
        print(f"Cloudinary upload mislukt ({e}), fallback naar catbox.moe...")
        return upload_to_catbox(filepath)


def upload_to_catbox(filepath):
    """Upload afbeelding naar catbox.moe (gratis, geen account nodig)."""
    import requests

    print("Uploading naar catbox.moe...")
    with open(filepath, "rb") as f:
        response = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload"},
            files={"fileToUpload": f},
            timeout=60,
        )

    if response.status_code == 200 and response.text.startswith("https://"):
        url = response.text.strip()
        print(f"URL:          {url}")
        return url
    else:
        print(f"Upload mislukt: {response.text}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Nano Banana Pro Image Generator")
    parser.add_argument("prompt", nargs="?", default=None,
                        help="Beschrijving van de gewenste afbeelding (niet nodig bij --client)")
    parser.add_argument("--model", default="gemini-3-pro-image-preview",
                        choices=["gemini-3-pro-image-preview", "gemini-2.5-flash-image", "imagen-4.0-generate-001"],
                        help="Gemini model (default: gemini-3-pro-image-preview)")
    parser.add_argument("--ratio", default="1:1",
                        choices=["1:1", "3:4", "4:3", "9:16", "16:9"],
                        help="Aspect ratio (default: 1:1)")
    parser.add_argument("--size", default="2K",
                        choices=["1K", "2K", "4K"],
                        help="Resolutie (default: 2K)")
    parser.add_argument("--output", default=None,
                        help="Output bestandspad (default: auto-generated)")
    parser.add_argument("--upload", action="store_true",
                        help="Upload naar catbox.moe en toon URL")
    parser.add_argument("--logo-domain", default=None,
                        help="Domein voor logo-download (bijv. coolblue.nl)")
    parser.add_argument("--json", action="store_true",
                        help="Output als JSON (voor scripts/automatie)")

    # Client-specifieke argumenten (AI-native aanpak)
    client_group = parser.add_argument_group("client mode",
                        "Genereer klantspecifieke AI Panda samenwerkingsafbeelding")
    client_group.add_argument("--client", action="store_true",
                        help="Activeer client mode: bouwt automatisch een klantspecifieke prompt")
    client_group.add_argument("--company-name", default=None,
                        help="Bedrijfsnaam (bijv. 'KPN')")
    client_group.add_argument("--sector", default=None,
                        help="Sector (telecom, retail, e-commerce, finance, zorg, logistiek, tech, onderwijs, energie, overheid)")
    client_group.add_argument("--brand-colors", default=None,
                        help="Brandkleuren als hex codes (bijv. '#00A83E,#FFFFFF')")

    # Legacy compositing
    parser.add_argument("--legacy-composite", action="store_true",
                        help="Gebruik legacy OpenCV badge-detectie + compositing i.p.v. AI-native")

    args = parser.parse_args()

    # Validatie
    if args.client and not args.company_name:
        parser.error("--client vereist --company-name")
    if not args.client and not args.prompt:
        parser.error("prompt is vereist (of gebruik --client met --company-name)")

    # Genereer bestandsnaam
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if args.client:
            safe_name = args.company_name.lower().replace(" ", "_")
            args.output = f"panda_{safe_name}_{timestamp}.png"
        else:
            args.output = f"generated_{timestamp}.png"

    # Logo ophalen via fallback-keten
    logo_path = None
    logo_img = None
    if args.logo_domain or args.client:
        company_for_logo = args.company_name if args.client else None
        logo_path, logo_img = resolve_logo(
            company_name=company_for_logo or args.logo_domain,
            domain=args.logo_domain,
        )

    # Bouw prompt
    if args.client:
        # AI-native client mode: bouw klantspecifieke prompt
        has_logo = logo_img is not None and not args.legacy_composite
        prompt = build_client_prompt(
            company_name=args.company_name,
            sector=args.sector,
            brand_colors=args.brand_colors,
            has_logo=has_logo,
        )
        print(f"Client mode:  {args.company_name} ({args.sector or 'tech'})")
    else:
        prompt = args.prompt

    # Laad panda character reference (altijd, voor consistentie)
    panda_ref_path = Path(__file__).parent.parent / "assets" / "panda-reference.png"
    panda_ref_img = None
    if panda_ref_path.exists():
        from PIL import Image as PILImage
        panda_ref_img = PILImage.open(panda_ref_path)
        print(f"Panda referentie: {panda_ref_path.name} geladen")
    elif args.client:
        print("WARNING: assets/panda-reference.png niet gevonden, karakter-consistentie niet gegarandeerd")

    # Referentie-images voor AI-native logo integratie: panda first, dan logo
    reference_images = None
    refs = []
    if panda_ref_img:
        refs.append(panda_ref_img)
    if logo_img and not args.legacy_composite:
        refs.append(logo_img)
        print("Logo wordt als referentie-image meegegeven aan Gemini (AI-native)")
    if refs:
        reference_images = refs

    # Genereer
    image_part, description = generate_image(
        prompt=prompt,
        model=args.model,
        aspect_ratio=args.ratio,
        image_size=args.size,
        reference_images=reference_images,
    )

    # Sla op
    filepath = save_image(image_part, args.output)

    # Legacy compositing (alleen als --legacy-composite flag)
    if args.legacy_composite and logo_path:
        badge_rect = detect_badge(filepath)
        if badge_rect:
            result_path = composite_logo(filepath, logo_path, badge_rect, filepath)
            if result_path:
                print("Legacy compositing succesvol!")
            else:
                print("Legacy compositing mislukt, originele afbeelding wordt gebruikt.")
        else:
            print("Geen badge gevonden, originele afbeelding wordt gebruikt.")

    # Cleanup temp logo file
    if logo_path:
        try:
            os.unlink(logo_path)
        except OSError:
            pass

    # Upload (optioneel)
    url = None
    if args.upload:
        url = upload_to_cloudinary(filepath)

    # JSON output voor automatie
    if args.json:
        result = {
            "filepath": filepath,
            "url": url,
            "description": description,
            "model": args.model,
            "prompt": args.prompt,
        }
        print(json.dumps(result, indent=2))
    elif description:
        print(f"Beschrijving: {description}")

    print("Klaar!")
    return url or filepath


if __name__ == "__main__":
    main()
