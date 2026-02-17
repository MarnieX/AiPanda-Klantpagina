"""Tests for the Gemini MCP image server (plugin/servers/gemini-image-server.py)."""

import json
import sys
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
import base64

import pytest
import pytest_asyncio

# Add plugin/servers to path
SERVERS_DIR = Path(__file__).parent.parent.parent / "plugin" / "servers"
sys.path.insert(0, str(SERVERS_DIR))


@pytest.mark.integration
class TestGenerateWithGemini:
    """Test the generate_with_gemini async function."""

    @pytest.mark.asyncio
    async def test_returns_none_without_api_key(self):
        """Without GEMINI_API_KEY, should return None immediately."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": ""}, clear=False):
            # Re-import to pick up empty key
            if "gemini-image-server" in sys.modules:
                del sys.modules["gemini-image-server"]
            # Mock mcp dependency
            mock_mcp = MagicMock()
            mock_mcp.server.fastmcp.FastMCP = MagicMock()
            with patch.dict("sys.modules", {"mcp": mock_mcp, "mcp.server": mock_mcp.server, "mcp.server.fastmcp": mock_mcp.server.fastmcp}):
                import importlib
                server = importlib.import_module("gemini-image-server")
                # Manually set the key to empty
                original_key = server.GEMINI_API_KEY
                server.GEMINI_API_KEY = ""
                try:
                    result = await server.generate_with_gemini("test prompt")
                    assert result is None
                finally:
                    server.GEMINI_API_KEY = original_key

    @pytest.mark.asyncio
    async def test_parses_inline_data_from_response(self):
        """Should correctly extract base64 image data from Gemini response."""
        fake_image_bytes = b"fake-png-data"
        fake_b64 = base64.b64encode(fake_image_bytes).decode()

        fake_response = {
            "candidates": [{
                "content": {
                    "parts": [
                        {"text": "Here is your image"},
                        {"inlineData": {"mimeType": "image/png", "data": fake_b64}},
                    ]
                }
            }]
        }

        mock_mcp = MagicMock()
        mock_mcp.server.fastmcp.FastMCP = MagicMock()
        with patch.dict("sys.modules", {"mcp": mock_mcp, "mcp.server": mock_mcp.server, "mcp.server.fastmcp": mock_mcp.server.fastmcp}):
            if "gemini-image-server" in sys.modules:
                del sys.modules["gemini-image-server"]
            import importlib
            server = importlib.import_module("gemini-image-server")
            server.GEMINI_API_KEY = "fake-key"

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = fake_response

            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)

            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await server.generate_with_gemini("test prompt")
                assert result == fake_image_bytes


@pytest.mark.integration
class TestGeneratePandaImage:
    """Test the generate_panda_image MCP tool."""

    @pytest.mark.asyncio
    async def test_success_returns_json_with_url(self):
        """Successful generation should return JSON with success=True and image_url."""
        mock_mcp = MagicMock()
        mock_mcp.server.fastmcp.FastMCP = MagicMock()
        mock_mcp_instance = MagicMock()
        mock_mcp_instance.tool = MagicMock(return_value=lambda f: f)
        mock_mcp.server.fastmcp.FastMCP.return_value = mock_mcp_instance

        with patch.dict("sys.modules", {"mcp": mock_mcp, "mcp.server": mock_mcp.server, "mcp.server.fastmcp": mock_mcp.server.fastmcp}):
            if "gemini-image-server" in sys.modules:
                del sys.modules["gemini-image-server"]
            import importlib
            server = importlib.import_module("gemini-image-server")

            with patch.object(server, "generate_with_gemini", new_callable=AsyncMock) as mock_gen, \
                 patch.object(server, "upload_to_catbox", new_callable=AsyncMock) as mock_upload:
                mock_gen.return_value = b"fake-image"
                mock_upload.return_value = "https://catbox.moe/test.png"

                result = await server.generate_panda_image("TestBV")
                data = json.loads(result)
                assert data["success"] is True
                assert data["image_url"] == "https://catbox.moe/test.png"
                assert data["bedrijfsnaam"] == "TestBV"

    @pytest.mark.asyncio
    async def test_gemini_failure_returns_fallback(self):
        """When Gemini returns no image, should return fallback URL."""
        mock_mcp = MagicMock()
        mock_mcp.server.fastmcp.FastMCP = MagicMock()
        mock_mcp_instance = MagicMock()
        mock_mcp_instance.tool = MagicMock(return_value=lambda f: f)
        mock_mcp.server.fastmcp.FastMCP.return_value = mock_mcp_instance

        with patch.dict("sys.modules", {"mcp": mock_mcp, "mcp.server": mock_mcp.server, "mcp.server.fastmcp": mock_mcp.server.fastmcp}):
            if "gemini-image-server" in sys.modules:
                del sys.modules["gemini-image-server"]
            import importlib
            server = importlib.import_module("gemini-image-server")

            with patch.object(server, "generate_with_gemini", new_callable=AsyncMock) as mock_gen:
                mock_gen.return_value = None

                result = await server.generate_panda_image("TestBV")
                data = json.loads(result)
                assert data["success"] is False
                assert "fallback_url" in data

    @pytest.mark.asyncio
    async def test_upload_failure_returns_fallback(self):
        """When upload fails, should return fallback URL."""
        mock_mcp = MagicMock()
        mock_mcp.server.fastmcp.FastMCP = MagicMock()
        mock_mcp_instance = MagicMock()
        mock_mcp_instance.tool = MagicMock(return_value=lambda f: f)
        mock_mcp.server.fastmcp.FastMCP.return_value = mock_mcp_instance

        with patch.dict("sys.modules", {"mcp": mock_mcp, "mcp.server": mock_mcp.server, "mcp.server.fastmcp": mock_mcp.server.fastmcp}):
            if "gemini-image-server" in sys.modules:
                del sys.modules["gemini-image-server"]
            import importlib
            server = importlib.import_module("gemini-image-server")

            with patch.object(server, "generate_with_gemini", new_callable=AsyncMock) as mock_gen, \
                 patch.object(server, "upload_to_catbox", new_callable=AsyncMock) as mock_upload:
                mock_gen.return_value = b"fake-image"
                mock_upload.return_value = ""

                result = await server.generate_panda_image("TestBV")
                data = json.loads(result)
                assert data["success"] is False
                assert "fallback_url" in data


@pytest.mark.integration
class TestGenerateCustomImage:
    """Test the generate_custom_image MCP tool."""

    @pytest.mark.asyncio
    async def test_success_returns_url(self):
        """Successful generation returns JSON with image_url."""
        mock_mcp = MagicMock()
        mock_mcp.server.fastmcp.FastMCP = MagicMock()
        mock_mcp_instance = MagicMock()
        mock_mcp_instance.tool = MagicMock(return_value=lambda f: f)
        mock_mcp.server.fastmcp.FastMCP.return_value = mock_mcp_instance

        with patch.dict("sys.modules", {"mcp": mock_mcp, "mcp.server": mock_mcp.server, "mcp.server.fastmcp": mock_mcp.server.fastmcp}):
            if "gemini-image-server" in sys.modules:
                del sys.modules["gemini-image-server"]
            import importlib
            server = importlib.import_module("gemini-image-server")

            with patch.object(server, "generate_with_gemini", new_callable=AsyncMock) as mock_gen, \
                 patch.object(server, "upload_to_catbox", new_callable=AsyncMock) as mock_upload:
                mock_gen.return_value = b"fake-image"
                mock_upload.return_value = "https://catbox.moe/custom.png"

                result = await server.generate_custom_image("a beautiful sunset")
                data = json.loads(result)
                assert data["success"] is True
                assert data["image_url"] == "https://catbox.moe/custom.png"

    @pytest.mark.asyncio
    async def test_failure_has_no_fallback_url(self):
        """Unlike panda, custom image failure should NOT include fallback_url."""
        mock_mcp = MagicMock()
        mock_mcp.server.fastmcp.FastMCP = MagicMock()
        mock_mcp_instance = MagicMock()
        mock_mcp_instance.tool = MagicMock(return_value=lambda f: f)
        mock_mcp.server.fastmcp.FastMCP.return_value = mock_mcp_instance

        with patch.dict("sys.modules", {"mcp": mock_mcp, "mcp.server": mock_mcp.server, "mcp.server.fastmcp": mock_mcp.server.fastmcp}):
            if "gemini-image-server" in sys.modules:
                del sys.modules["gemini-image-server"]
            import importlib
            server = importlib.import_module("gemini-image-server")

            with patch.object(server, "generate_with_gemini", new_callable=AsyncMock) as mock_gen:
                mock_gen.return_value = None

                result = await server.generate_custom_image("test")
                data = json.loads(result)
                assert data["success"] is False
                assert "fallback_url" not in data
