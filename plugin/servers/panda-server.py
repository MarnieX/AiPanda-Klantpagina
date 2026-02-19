#!/usr/bin/env python3
"""
MCP server voor AI Panda plugin.
- AI-beeldgeneratie via Google Gemini
- Image upload naar 0x0.st / catbox.moe
- Team Excel uitlezen
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
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "httpcore[socks]", "--break-system-packages", "-q"])
    import httpx

try:
    import openpyxl
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "--break-system-packages", "-q"])
    import openpyxl


mcp = FastMCP("panda-server")

# GEMINI_API_KEY is passed via .mcp.json from the environment.
# In Cowork/CLI this is set by ~/.claude/settings.json.
# Fallback: .env in project root (local development only).
if not os.environ.get("GEMINI_API_KEY"):
    try:
        from dotenv import load_dotenv
        _env = Path(__file__).parent.parent.parent / ".env"
        if _env.exists():
            load_dotenv(_env)
    except ImportError:
        pass

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3-pro-image-preview"
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


async def upload_to_0x0(tmp_path: str) -> str:
    """Upload a file to 0x0.st and return the public URL."""
    result = subprocess.run(
        ["curl", "-s", "-F", f"file=@{tmp_path}", "https://0x0.st"],
        capture_output=True, text=True, timeout=30,
    )
    url = result.stdout.strip()
    return url if url.startswith("http") else ""


async def upload_to_catbox(tmp_path: str) -> str:
    """Upload a file to catbox.moe and return the public URL."""
    result = subprocess.run(
        ["curl", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{tmp_path}",
         "https://catbox.moe/user/api.php"],
        capture_output=True, text=True, timeout=30,
    )
    url = result.stdout.strip()
    return url if url.startswith("http") else ""


async def upload_image(image_bytes: bytes, filename: str = "image.png") -> str:
    """Upload image bytes to a public host. Tries 0x0.st first, catbox.moe as fallback."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(image_bytes)
        tmp_path = f.name

    try:
        url = await upload_to_0x0(tmp_path)
        if url:
            return url
        url = await upload_to_catbox(tmp_path)
        if url:
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

        url = await upload_image(image_bytes, f"panda_{bedrijfsnaam.lower().replace(' ', '_')}.png")
        if not url:
            return json.dumps({
                "success": False,
                "error": "Upload mislukt (0x0.st en catbox.moe beide gefaald).",
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

        url = await upload_image(image_bytes)
        if not url:
            return json.dumps({"success": False, "error": "Upload mislukt."})

        return json.dumps({"success": True, "image_url": url})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
async def upload_image_base64(image_base64: str, filename: str = "image.png") -> str:
    """
    Upload base64-encoded image data en retourneer een publieke URL.
    Probeert 0x0.st (primair) en catbox.moe (fallback). Server-side upload, geen CORS.

    Args:
        image_base64: Base64-encoded image data (zonder data:... prefix).
        filename: Gewenste bestandsnaam (default: image.png).
    """
    try:
        image_bytes = base64.b64decode(image_base64)
        url = await upload_image(image_bytes, filename)
        if not url:
            return json.dumps({"success": False, "error": "Upload mislukt (0x0.st en catbox.moe beide gefaald)."})
        return json.dumps({"success": True, "image_url": url})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
async def read_team_excel() -> str:
    """
    Lees het AI Panda teambestand (ai-panda-team.xlsx) en retourneer alle teamleden als JSON.
    Zoekt automatisch op de juiste locatie (CLAUDE_PLUGIN_ROOT of find fallback).

    Retourneert: JSON array met objecten: [{naam, functie, foto_url, telefoon, email}, ...]
    Bij fout: JSON object met error en searched_paths.
    """
    searched_paths = []

    # Primary: CLAUDE_PLUGIN_ROOT (most reliable in Cowork)
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root:
        candidate = Path(plugin_root) / "data" / "ai-panda-team.xlsx"
        searched_paths.append(str(candidate))
        if candidate.exists():
            return _read_excel(candidate)

    # Fallback: relative to this script (local development)
    script_relative = Path(__file__).parent.parent / "data" / "ai-panda-team.xlsx"
    searched_paths.append(str(script_relative))
    if script_relative.exists():
        return _read_excel(script_relative)

    # Fallback: find with timeout
    try:
        result = subprocess.run(
            ["find", "/sessions", str(Path.home()), "-maxdepth", "3", "-name", "ai-panda-team.xlsx"],
            capture_output=True, text=True, timeout=5,
        )
        for line in result.stdout.strip().splitlines():
            path = Path(line.strip())
            searched_paths.append(str(path))
            if path.exists():
                return _read_excel(path)
    except (subprocess.TimeoutExpired, Exception):
        pass

    return json.dumps({
        "error": "ai-panda-team.xlsx niet gevonden",
        "searched_paths": searched_paths,
    })


def _read_excel(path: Path) -> str:
    """Parse the team Excel file and return JSON."""
    try:
        wb = openpyxl.load_workbook(path)
        ws = wb.active

        headers = [str(cell or "").strip().lower() for cell in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
        team = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                entry = {}
                for i, h in enumerate(headers):
                    entry[h] = str(row[i] or "") if i < len(row) else ""
                team.append({
                    "naam": entry.get("naam", ""),
                    "functie": entry.get("functie", ""),
                    "foto_url": entry.get("foto-url", entry.get("foto_url", "")),
                    "telefoon": entry.get("telefoon", ""),
                    "email": entry.get("e-mail", entry.get("email", "")),
                })
        return json.dumps(team, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Excel lezen mislukt: {e}", "path": str(path)})


if __name__ == "__main__":
    mcp.run()
