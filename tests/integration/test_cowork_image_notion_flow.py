"""Critical Cowork simulation tests: image generation -> Notion payload."""

import importlib.util
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.helpers.notion_payload import (
    build_notion_create_pages_payload,
    render_klantpagina_template,
)

SERVER_PATH = Path(__file__).parent.parent.parent / "plugin" / "servers" / "panda-server.py"
TEMPLATE_PATH = Path(__file__).parent.parent.parent / "plugin" / "templates" / "klantpagina.md"


def _load_server_module():
    mock_mcp = MagicMock()
    mock_mcp.server.fastmcp.FastMCP = MagicMock()
    mock_mcp_instance = MagicMock()
    mock_mcp_instance.tool = MagicMock(return_value=lambda f: f)
    mock_mcp.server.fastmcp.FastMCP.return_value = mock_mcp_instance

    spec = importlib.util.spec_from_file_location("cowork_panda_server_under_test", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    with patch.dict("sys.modules", {
        "mcp": mock_mcp,
        "mcp.server": mock_mcp.server,
        "mcp.server.fastmcp": mock_mcp.server.fastmcp,
    }):
        spec.loader.exec_module(module)
    return module


def _base_fields(image_url: str) -> dict:
    return {
        "PANDA_IMAGE_URL": image_url,
        "BEDRIJFSNAAM": "Coolblue",
        "MEDEWERKER_QUOTE": "AI doet nu het uitzoekwerk waar ik vroeger uren op zat.",
        "OMSCHRIJVING": "Coolblue is een Nederlandse e-commerce retailer.",
        "SECTOR": "Retail",
        "WEBSITE_DOMEIN": "coolblue.nl",
        "ROADMAP_FASE_1": "Discovery voor klantenservice en orderdata.",
        "ROADMAP_FASE_2": "Pilot op retourpredictie en assistentflows.",
        "ROADMAP_FASE_3": "Implementatie in service en operatie.",
        "ROADMAP_FASE_4": "Schalen met continue optimalisatie.",
        "QUIZ_URL": "https://marniex.github.io/aipanda-quiz/#data=abc",
        "DATUM": "19 februari 2026",
    }


def _consultants() -> list[dict]:
    return [
        {
            "naam": "Marnix",
            "functie": "Consultant",
            "telefoon": "0612345678",
            "email": "marnix@aipanda.nl",
            "foto_url": "https://files.catbox.moe/marnix.png",
        },
        {
            "naam": "Rick",
            "functie": "AI Consultant",
            "telefoon": "0687654321",
            "email": "rick@aipanda.nl",
            "foto_url": "https://files.catbox.moe/rick.png",
        },
    ]


@pytest.mark.integration
@pytest.mark.cowork
@pytest.mark.asyncio
async def test_image_generation_to_notion_payload_happy_path():
    server = _load_server_module()
    with patch.object(server, "_fetch_logo_b64", return_value=None), \
         patch.object(server, "generate_with_gemini", new_callable=AsyncMock) as mock_gemini, \
         patch.object(server, "upload_image", new_callable=AsyncMock) as mock_upload:
        mock_gemini.return_value = b"image-bytes"
        mock_upload.return_value = "https://files.catbox.moe/panda-coolblue.png"
        image_result = json.loads(await server.generate_panda_image("Coolblue", "Retail", "coolblue.nl"))

    assert image_result["success"] is True
    image_url = image_result["image_url"]

    content = render_klantpagina_template(TEMPLATE_PATH, _base_fields(image_url), _consultants())
    payload = build_notion_create_pages_payload("Coolblue", content)

    assert payload["title"] == "AI Panda x Coolblue"
    assert "![](https://files.catbox.moe/panda-coolblue.png)" in payload["content"]
    assert "[PANDA_IMAGE_URL]" not in payload["content"]
    assert "![]()" not in payload["content"]


@pytest.mark.integration
@pytest.mark.cowork
def test_image_failure_omits_hero_image_line():
    content = render_klantpagina_template(TEMPLATE_PATH, _base_fields(""), _consultants())
    payload = build_notion_create_pages_payload("Coolblue", content)

    # Hero image line should be omitted when no PANDA_IMAGE_URL is available.
    first_nonempty = next(line for line in payload["content"].splitlines() if line.strip())
    assert not first_nonempty.startswith("![](")
    assert payload["content"].lstrip().startswith("# AI Panda x Coolblue")
