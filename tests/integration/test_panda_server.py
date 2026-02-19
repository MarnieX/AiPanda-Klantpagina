"""Integration-style tests for plugin/servers/panda-server.py."""

import base64
import importlib.util
import json
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

SERVER_PATH = Path(__file__).parent.parent.parent / "plugin" / "servers" / "panda-server.py"


def _load_server(env=None):
    """Load panda-server.py as a module with a mocked MCP dependency."""
    mock_mcp = MagicMock()
    mock_mcp.server.fastmcp.FastMCP = MagicMock()
    mock_mcp_instance = MagicMock()
    mock_mcp_instance.tool = MagicMock(return_value=lambda f: f)
    mock_mcp.server.fastmcp.FastMCP.return_value = mock_mcp_instance

    spec = importlib.util.spec_from_file_location("panda_server_under_test", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)

    with patch.dict("sys.modules", {
        "mcp": mock_mcp,
        "mcp.server": mock_mcp.server,
        "mcp.server.fastmcp": mock_mcp.server.fastmcp,
    }):
        with patch.dict(os.environ, env or {}, clear=False):
            spec.loader.exec_module(module)
    return module


@pytest.mark.integration
class TestApiKeyTools:
    @pytest.mark.asyncio
    async def test_check_api_keys_reflects_env(self):
        server = _load_server({"GEMINI_API_KEY": "g-key", "OPENAI_API_KEY": ""})
        data = json.loads(await server.check_api_keys())
        assert data["gemini"] is True
        assert data["openai"] is False

    @pytest.mark.asyncio
    async def test_set_api_key_updates_memory_state(self):
        server = _load_server({"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""})
        result = json.loads(await server.set_api_key("gemini", "abc123"))
        assert result["success"] is True
        data = json.loads(await server.check_api_keys())
        assert data["gemini"] is True


@pytest.mark.integration
class TestImageGeneration:
    @pytest.mark.asyncio
    async def test_generate_with_gemini_returns_none_without_key(self):
        server = _load_server({"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""})
        server._gemini_api_key = ""
        result = await server.generate_with_gemini("test prompt")
        assert result is None

    @pytest.mark.asyncio
    async def test_generate_with_gemini_parses_inline_data(self):
        server = _load_server({"GEMINI_API_KEY": "g-key"})
        fake_image_bytes = b"fake-png-data"
        fake_b64 = base64.b64encode(fake_image_bytes).decode()
        fake_response = {
            "candidates": [{
                "content": {
                    "parts": [
                        {"text": "ok"},
                        {"inlineData": {"mimeType": "image/png", "data": fake_b64}},
                    ]
                }
            }]
        }

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = fake_response
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        server._gemini_api_key = "g-key"
        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await server.generate_with_gemini("test prompt")
        assert result == fake_image_bytes

    @pytest.mark.asyncio
    async def test_generate_panda_image_returns_success(self):
        server = _load_server({"GEMINI_API_KEY": "g-key"})
        with patch.object(server, "_fetch_logo_b64", return_value=None), \
             patch.object(server, "generate_with_gemini", new_callable=AsyncMock) as mock_gen, \
             patch.object(server, "upload_image", new_callable=AsyncMock) as mock_upload:
            mock_gen.return_value = b"image-bytes"
            mock_upload.return_value = "https://files.catbox.moe/test.png"
            data = json.loads(await server.generate_panda_image("TestBV"))
        assert data["success"] is True
        assert data["provider"] == "gemini"

    @pytest.mark.asyncio
    async def test_generate_custom_image_failure_has_no_fallback_url(self):
        server = _load_server({"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""})
        with patch.object(server, "generate_with_gemini", new_callable=AsyncMock, return_value=None), \
             patch.object(server, "generate_with_openai", new_callable=AsyncMock, return_value=None):
            data = json.loads(await server.generate_custom_image("test"))
        assert data["success"] is False
        assert "fallback_url" not in data


@pytest.mark.integration
class TestExcelReading:
    @pytest.mark.asyncio
    async def test_read_team_excel_via_plugin_root(self, tmp_path):
        try:
            from openpyxl import Workbook
        except ImportError:
            pytest.skip("openpyxl not installed")

        data_dir = tmp_path / "data"
        data_dir.mkdir()
        xlsx = data_dir / "ai-panda-team.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.append(["Naam", "Functie", "Team", "Telefoon", "Foto URL", "Email"])
        ws.append(["Alice", "Developer", "Alpha", "06123", "https://img/alice.png", "alice@test.nl"])
        wb.save(xlsx)

        server = _load_server()
        with patch.dict(os.environ, {"CLAUDE_PLUGIN_ROOT": str(tmp_path)}, clear=False):
            payload = json.loads(await server.read_team_excel())
        assert isinstance(payload, list)
        assert payload[0]["naam"] == "Alice"
        assert payload[0]["functie"] == "Developer"
