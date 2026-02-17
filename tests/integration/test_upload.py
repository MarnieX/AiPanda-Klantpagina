"""Tests for upload_to_catbox() and upload_to_cloudinary() in generate_notion_image.py."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

import generate_notion_image as gni


@pytest.fixture
def temp_image_file():
    """Create a temporary file simulating an image."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        path = f.name
    yield path
    Path(path).unlink(missing_ok=True)


@pytest.mark.integration
class TestUploadToCatbox:
    """Test catbox.moe upload logic."""

    @patch("requests.post")
    def test_success_returns_url(self, mock_post, temp_image_file):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "https://files.catbox.moe/abc123.png"
        mock_post.return_value = mock_response

        result = gni.upload_to_catbox(temp_image_file)
        assert result == "https://files.catbox.moe/abc123.png"

    @patch("requests.post")
    def test_non_https_response_returns_none(self, mock_post, temp_image_file):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "error: rate limited"
        mock_post.return_value = mock_response

        result = gni.upload_to_catbox(temp_image_file)
        assert result is None

    @patch("requests.post")
    def test_failed_status_returns_none(self, mock_post, temp_image_file):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        result = gni.upload_to_catbox(temp_image_file)
        assert result is None


@pytest.mark.integration
class TestUploadToCloudinary:
    """Test cloudinary upload with fallback logic."""

    @patch.dict("os.environ", {}, clear=True)
    @patch.object(gni, "upload_to_catbox", return_value="https://catbox.moe/fallback.png")
    def test_missing_env_vars_falls_back_to_catbox(self, mock_catbox, temp_image_file):
        result = gni.upload_to_cloudinary(temp_image_file)
        mock_catbox.assert_called_once_with(temp_image_file)
        assert result == "https://catbox.moe/fallback.png"

    @patch.dict("os.environ", {"CLOUDINARY_CLOUD_NAME": "test"}, clear=True)
    @patch.object(gni, "upload_to_catbox", return_value=None)
    def test_partial_env_vars_falls_back_to_catbox(self, mock_catbox, temp_image_file):
        """Only one of three Cloudinary vars set should trigger fallback."""
        result = gni.upload_to_cloudinary(temp_image_file)
        mock_catbox.assert_called_once()

    @patch.dict("os.environ", {
        "CLOUDINARY_CLOUD_NAME": "test",
        "CLOUDINARY_API_KEY": "key",
        "CLOUDINARY_API_SECRET": "secret",
    }, clear=True)
    @patch.object(gni, "upload_to_catbox", return_value="https://catbox.moe/fallback.png")
    def test_import_error_falls_back_to_catbox(self, mock_catbox, temp_image_file):
        """When cloudinary package is not installed, fall back to catbox."""
        with patch.dict("sys.modules", {"cloudinary": None, "cloudinary.uploader": None}):
            result = gni.upload_to_cloudinary(temp_image_file)
            mock_catbox.assert_called_once()
