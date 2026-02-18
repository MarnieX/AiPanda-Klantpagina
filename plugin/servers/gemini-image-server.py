#!/usr/bin/env python3
"""
MCP server voor AI-beeldgeneratie via Google Gemini.
Genereert afbeeldingen en upload ze naar catbox.moe voor publieke URLs.
"""

import asyncio
import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Ensure dependencies
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp[cli]", "--break-system-packages", "-q"])
    from mcp.server.fastmcp import FastMCP

try:
    import httpx
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "--break-system-packages", "-q"])
    import httpx


mcp = FastMCP("gemini-image-generator")

# Load GEMINI_API_KEY. Priority:
# 1. Environment variable (set by Claude Code settings.json, Cowork, or shell)
# 2. .env file fallback (local development)
#
# Recommended: configure via ~/.claude/settings.json:
#   {"env": {"GEMINI_API_KEY": "your-key"}}
if not os.environ.get("GEMINI_API_KEY"):
    try:
        from dotenv import load_dotenv
        _env_paths = [
            Path(__file__).parent.parent.parent / ".env",  # plugin project root
            Path(__file__).parent.parent / ".env",          # plugin/
            Path(__file__).parent / ".env",                 # servers/
            Path.home() / ".env",                           # home directory
            Path.home() / ".claude" / ".env",               # claude config dir
        ]
        for _p in _env_paths:
            if _p.exists():
                load_dotenv(_p)
                if os.environ.get("GEMINI_API_KEY"):
                    break
    except ImportError:
        pass  # dotenv is optional

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash-exp"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


async def generate_with_gemini(prompt: str) -> bytes | None:
    """Generate an image using Google Gemini API."""
    if not GEMINI_API_KEY:
        return None

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            GEMINI_URL,
            params={"key": GEMINI_API_KEY},
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    # Extract image from response
    for candidate in data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])
    return None


async def upload_to_catbox(image_bytes: bytes, filename: str = "image.png") -> str:
    """Upload image bytes to catbox.moe and return the public URL."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(image_bytes)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["curl", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{tmp_path}",
             "https://catbox.moe/user/api.php"],
            capture_output=True, text=True, timeout=30,
        )
        url = result.stdout.strip()
        if url.startswith("http"):
            return url
        return ""
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@mcp.tool()
async def generate_panda_image(bedrijfsnaam: str) -> str:
    """
    Genereer een AI Panda mascotte-afbeelding met de bedrijfsnaam op het shirt.
    Retourneert een publieke URL naar de afbeelding.

    Args:
        bedrijfsnaam: De naam van het bedrijf die op het panda-shirt komt.
    """
    prompt = (
        f"A cute, friendly cartoon panda mascot (the AI Panda) standing proudly "
        f"and giving a thumbs up. The panda wears a modern t-shirt with the text "
        f"'{bedrijfsnaam}' clearly printed on the chest in bold letters. Big "
        f"expressive eyes, rosy cheeks, clean cartoon illustration style, white "
        f"background, professional but playful."
    )

    try:
        image_bytes = await generate_with_gemini(prompt)
        if not image_bytes:
            return json.dumps({
                "success": False,
                "error": "Gemini API gaf geen afbeelding terug. Controleer je GEMINI_API_KEY.",
                "fallback_url": f"https://ui-avatars.com/api/?name=AI+Panda&size=400&background=000000&color=ffffff&bold=true&format=png",
            })

        url = await upload_to_catbox(image_bytes, f"panda_{bedrijfsnaam.lower().replace(' ', '_')}.png")
        if not url:
            return json.dumps({
                "success": False,
                "error": "Upload naar catbox.moe mislukt.",
                "fallback_url": f"https://ui-avatars.com/api/?name=AI+Panda&size=400&background=000000&color=ffffff&bold=true&format=png",
            })

        return json.dumps({
            "success": True,
            "image_url": url,
            "bedrijfsnaam": bedrijfsnaam,
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "fallback_url": f"https://ui-avatars.com/api/?name=AI+Panda&size=400&background=000000&color=ffffff&bold=true&format=png",
        })


@mcp.tool()
async def generate_custom_image(prompt: str) -> str:
    """
    Genereer een willekeurige afbeelding via Google Gemini en retourneer een publieke URL.

    Args:
        prompt: Beschrijving van de gewenste afbeelding (in het Engels voor beste resultaten).
    """
    try:
        image_bytes = await generate_with_gemini(prompt)
        if not image_bytes:
            return json.dumps({"success": False, "error": "Geen afbeelding gegenereerd."})

        url = await upload_to_catbox(image_bytes)
        if not url:
            return json.dumps({"success": False, "error": "Upload mislukt."})

        return json.dumps({"success": True, "image_url": url})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


if __name__ == "__main__":
    mcp.run()
