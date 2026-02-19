#!/usr/bin/env python3
"""
🍌 Nano Banana Pro — Prompt Optimizer
======================================
Neemt een simpele beschrijving en maakt er een geoptimaliseerde
Gemini-prompt van, klaar om te genereren.

Gebruik:
  python prompt-optimizer.py "een panda in een bamboe bos" --stijl cartoon
  python prompt-optimizer.py "berglandschap" --stijl foto --ratio 16:9
  python prompt-optimizer.py "logo voor koffieshop" --stijl logo --tekst "Morning Brew"

Dit script slaat het resultaat op als .txt in de prompts/ map,
zodat nano-banana-generate.sh het automatisch oppikt.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# === PROMPT TEMPLATES (gebaseerd op Gemini best practices) ===

TEMPLATES = {
    "cartoon": {
        "name": "Cartoon / Illustratie",
        "template": (
            "A charming {substyle} illustration of {subject}. "
            "The character has big, expressive eyes with a warm sparkle, "
            "{extra_features}. "
            "The style is {mood}, with bold clean outlines, smooth cel-shading, "
            "and rounded proportions that give a cuddly, approachable look. "
            "The colour palette is {palette}. "
            "{background}. "
            "{aspect_hint}"
        ),
        "defaults": {
            "substyle": "cartoon",
            "mood": "soft and friendly",
            "palette": "warm and inviting with soft, natural tones",
            "extra_features": "rosy cheeks, and a gentle smile",
            "background": "The background features a dreamy, slightly blurred scene with soft golden sunlight",
        },
    },
    "foto": {
        "name": "Fotorealistisch",
        "template": (
            "A photorealistic {shot_type} of {subject}, {action}. "
            "Set in {environment}. "
            "The scene is illuminated by {lighting}, creating a {mood} atmosphere. "
            "Captured with {camera}, emphasizing {details}. "
            "{aspect_hint}"
        ),
        "defaults": {
            "shot_type": "medium shot",
            "action": "in a natural, candid moment",
            "environment": "a beautiful natural setting",
            "lighting": "soft, golden hour light",
            "mood": "serene and atmospheric",
            "camera": "an 85mm portrait lens with soft bokeh",
            "details": "fine textures and natural details",
        },
    },
    "logo": {
        "name": "Logo / Minimalistisch",
        "template": (
            'Create a modern, minimalist logo design featuring {subject}. '
            '{text_instruction}'
            "The design should be {style_desc}, with a {palette}. "
            "Clean lines, simple shapes, professional look. "
            "The background must be white or transparent. "
            "{aspect_hint}"
        ),
        "defaults": {
            "style_desc": "clean, bold, and contemporary",
            "palette": "colour scheme of two to three complementary tones",
        },
    },
    "artistiek": {
        "name": "Artistiek / Schilderij",
        "template": (
            "An artistic {art_style} painting of {subject}. "
            "The composition features {composition}. "
            "Rendered with {technique}, creating a {mood} mood. "
            "The colour palette emphasizes {palette}. "
            "{background}. "
            "{aspect_hint}"
        ),
        "defaults": {
            "art_style": "impressionist oil",
            "composition": "a balanced, dynamic arrangement with natural depth",
            "technique": "visible brushstrokes and rich, layered pigments",
            "mood": "dreamy and evocative",
            "palette": "warm golden tones with cool blue accents",
            "background": "The background blends soft, atmospheric washes of colour",
        },
    },
}

RATIO_HINTS = {
    "1:1": "Square image.",
    "16:9": "Landscape, widescreen format.",
    "9:16": "Vertical portrait orientation.",
    "4:3": "Standard landscape format.",
    "3:4": "Standard portrait format.",
}


def optimize_prompt(description, stijl="cartoon", ratio="1:1", tekst=None):
    """Neem een simpele beschrijving en maak er een geoptimaliseerde prompt van."""

    template_data = TEMPLATES.get(stijl, TEMPLATES["cartoon"])
    template = template_data["template"]
    defaults = template_data["defaults"].copy()

    # Vul subject in
    defaults["subject"] = description
    defaults["aspect_hint"] = RATIO_HINTS.get(ratio, "Square image.")

    # Tekst-specifieke instructie voor logo's
    if tekst and stijl == "logo":
        defaults["text_instruction"] = (
            f'The text "{tekst}" should be rendered in a clean, bold, sans-serif font, '
            f"seamlessly integrated with the icon. "
        )
    else:
        defaults["text_instruction"] = ""

    # Bouw de prompt
    prompt = template.format(**defaults)

    # Clean up dubbele spaties
    prompt = " ".join(prompt.split())

    return prompt


def save_prompt(prompt, stijl, ratio, model="gemini-3-pro-image-preview"):
    """Sla prompt op als .txt bestand in de prompts/ map."""
    script_dir = Path(__file__).parent
    prompts_dir = script_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prompt_{stijl}_{timestamp}.txt"
    filepath = prompts_dir / filename

    content = f"{prompt}\nmodel:{model}\nratio:{ratio}\n"
    filepath.write_text(content)

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="🍌 Nano Banana Pro — Prompt Optimizer"
    )
    parser.add_argument("beschrijving", help="Simpele beschrijving van de gewenste afbeelding")
    parser.add_argument(
        "--stijl", "-s",
        default="cartoon",
        choices=["cartoon", "foto", "logo", "artistiek"],
        help="Visuele stijl (default: cartoon)",
    )
    parser.add_argument(
        "--ratio", "-r",
        default="1:1",
        choices=["1:1", "3:4", "4:3", "9:16", "16:9"],
        help="Aspect ratio (default: 1:1)",
    )
    parser.add_argument(
        "--model", "-m",
        default="gemini-3-pro-image-preview",
        choices=["gemini-3-pro-image-preview", "gemini-3-pro-image-preview", "gemini-3-pro-image-preview"],
        help="Gemini model (default: gemini-3-pro-image-preview)",
    )
    parser.add_argument(
        "--tekst", "-t",
        default=None,
        help="Tekst om in de afbeelding te renderen (voor logo's/posters)",
    )
    parser.add_argument(
        "--generate", "-g",
        action="store_true",
        help="Direct genereren na optimalisatie (voert nano-banana-generate.sh uit)",
    )

    args = parser.parse_args()

    # Optimaliseer
    print(f"🍌 Nano Banana Pro — Prompt Optimizer")
    print(f"   Stijl:        {TEMPLATES[args.stijl]['name']}")
    print(f"   Beschrijving: {args.beschrijving}")
    print(f"   Ratio:        {args.ratio}")
    if args.tekst:
        print(f"   Tekst:        {args.tekst}")
    print()

    prompt = optimize_prompt(
        description=args.beschrijving,
        stijl=args.stijl,
        ratio=args.ratio,
        tekst=args.tekst,
    )

    print(f"✨ Geoptimaliseerde prompt:")
    print(f"   {prompt}")
    print()

    # Sla op
    filepath = save_prompt(prompt, args.stijl, args.ratio, args.model)
    print(f"💾 Opgeslagen: {filepath}")

    # Direct genereren?
    if args.generate:
        print()
        script_dir = Path(__file__).parent
        generate_script = script_dir / "nano-banana-generate.sh"
        if generate_script.exists():
            os.system(f'"{generate_script}"')
        else:
            print("⚠️  nano-banana-generate.sh niet gevonden. Voer handmatig uit:")
            print(f'   python generate_notion_image.py "{prompt}" --ratio {args.ratio} --model {args.model}')

    return prompt


if __name__ == "__main__":
    main()
