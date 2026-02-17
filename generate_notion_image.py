#!/usr/bin/env python3
"""
Nano Banana Pro → Notion Pipeline
==================================
Genereert een afbeelding via Google Gemini API,
upload naar een image host, en retourneert de URL.

Gebruik:
  python generate_notion_image.py "een panda die code schrijft"
  python generate_notion_image.py "berglandschap bij zonsopgang" --ratio 16:9 --size 2K
  python generate_notion_image.py "abstract tech design" --model gemini-2.5-flash-preview-05-20

Vereisten:
  pip install google-genai Pillow python-dotenv requests opencv-python-headless

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
    """Laad API key uit .env bestand."""
    # Zoek .env in huidige map of bovenliggende mappen
    for p in [Path(".env"), Path(__file__).parent / ".env"]:
        if p.exists():
            load_dotenv(p)
            break

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY niet gevonden.")
        print("Maak een .env bestand met: GEMINI_API_KEY=jouw-key")
        print("Key aanmaken op: https://aistudio.google.com/apikey")
        sys.exit(1)
    return key


def generate_image(prompt, model="gemini-3-pro-image-preview", aspect_ratio="1:1", image_size="2K"):
    """Genereer afbeelding via Gemini API."""
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    print(f"Model:        {model}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"Image size:   {image_size}")
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

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
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


def download_logo(domain):
    """Download bedrijfslogo via Google Favicons API."""
    import requests

    url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
    print(f"Logo downloaden voor {domain}...")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        if len(response.content) < 100:
            print(f"WARNING: Logo te klein of niet gevonden voor {domain}")
            return None

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(response.content)
        tmp.close()
        print(f"Logo opgeslagen: {tmp.name} ({len(response.content):,} bytes)")
        return tmp.name
    except Exception as e:
        print(f"WARNING: Logo download mislukt voor {domain}: {e}")
        return None


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
    parser.add_argument("prompt", help="Beschrijving van de gewenste afbeelding")
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

    args = parser.parse_args()

    # Genereer bestandsnaam
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"generated_{timestamp}.png"

    # Genereer
    image_part, description = generate_image(
        prompt=args.prompt,
        model=args.model,
        aspect_ratio=args.ratio,
        image_size=args.size,
    )

    # Sla op
    filepath = save_image(image_part, args.output)

    # Logo compositing (optioneel)
    if args.logo_domain:
        logo_path = download_logo(args.logo_domain)
        if logo_path:
            badge_rect = detect_badge(filepath)
            if badge_rect:
                result_path = composite_logo(filepath, logo_path, badge_rect, filepath)
                if result_path:
                    print("Logo compositing succesvol!")
                else:
                    print("Logo compositing mislukt, originele afbeelding wordt gebruikt.")
            else:
                print("Geen badge gevonden, originele afbeelding wordt gebruikt.")
            # Cleanup temp logo file
            try:
                os.unlink(logo_path)
            except OSError:
                pass
        else:
            print("Logo niet beschikbaar, originele afbeelding wordt gebruikt.")

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
