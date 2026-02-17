"""Tests for resolve_logo() fallback chain in generate_notion_image.py."""

import pytest
from unittest.mock import patch, MagicMock
from PIL import Image

import generate_notion_image as gni


@pytest.fixture
def fake_logo():
    """Create a minimal PIL Image that passes MIN_LOGO_SIZE check."""
    return Image.new("RGBA", (100, 100), color="red")


@pytest.mark.integration
class TestResolveLogoChain:
    """Test the 4-step fallback chain for logo resolution."""

    @patch.object(gni, "_try_image_search", return_value=None)
    def test_without_domain_skips_first_three_steps(self, mock_search):
        """Without a domain, only image search (step 4) is attempted."""
        path, img = gni.resolve_logo("TestCompany", domain=None)
        mock_search.assert_called_once()
        assert path is None
        assert img is None

    @patch.object(gni, "_try_google_favicon")
    @patch.object(gni, "_try_website_scrape")
    @patch.object(gni, "_try_duckduckgo_favicon")
    @patch.object(gni, "_try_image_search")
    def test_stops_at_first_success(self, mock_search, mock_ddg, mock_scrape, mock_google, fake_logo):
        """Chain stops as soon as a step returns a valid image."""
        mock_google.return_value = fake_logo
        path, img = gni.resolve_logo("Test", domain="test.com")

        mock_google.assert_called_once()
        mock_scrape.assert_not_called()
        mock_ddg.assert_not_called()
        mock_search.assert_not_called()
        assert img is not None
        # Cleanup temp file
        if path:
            import os
            os.unlink(path)

    @patch.object(gni, "_try_google_favicon", return_value=None)
    @patch.object(gni, "_try_website_scrape")
    @patch.object(gni, "_try_duckduckgo_favicon")
    @patch.object(gni, "_try_image_search")
    def test_falls_through_on_failure(self, mock_search, mock_ddg, mock_scrape, mock_google, fake_logo):
        """When step 1 fails, step 2 is tried."""
        mock_scrape.return_value = fake_logo
        path, img = gni.resolve_logo("Test", domain="test.com")

        mock_google.assert_called_once()
        mock_scrape.assert_called_once()
        mock_ddg.assert_not_called()
        assert img is not None
        if path:
            import os
            os.unlink(path)

    @patch.object(gni, "_try_google_favicon", side_effect=Exception("network error"))
    @patch.object(gni, "_try_website_scrape", return_value=None)
    @patch.object(gni, "_try_duckduckgo_favicon", return_value=None)
    @patch.object(gni, "_try_image_search", return_value=None)
    def test_exception_does_not_stop_chain(self, mock_search, mock_ddg, mock_scrape, mock_google):
        """An exception in one step should not break the entire chain."""
        path, img = gni.resolve_logo("Test", domain="test.com")
        # All steps should have been attempted
        mock_google.assert_called_once()
        mock_scrape.assert_called_once()
        assert path is None
        assert img is None

    @patch.object(gni, "_try_google_favicon", return_value=None)
    @patch.object(gni, "_try_website_scrape", return_value=None)
    @patch.object(gni, "_try_duckduckgo_favicon", return_value=None)
    @patch.object(gni, "_try_image_search", return_value=None)
    def test_all_fail_returns_none_none(self, mock_search, mock_ddg, mock_scrape, mock_google):
        """When all steps fail, (None, None) is returned."""
        path, img = gni.resolve_logo("Test", domain="test.com")
        assert path is None
        assert img is None

    @patch.object(gni, "_try_google_favicon", return_value=None)
    @patch.object(gni, "_try_website_scrape", return_value=None)
    @patch.object(gni, "_try_duckduckgo_favicon", return_value=None)
    @patch.object(gni, "_try_image_search")
    def test_with_domain_tries_all_four_steps(self, mock_search, mock_ddg, mock_scrape, mock_google):
        """With a domain, all four steps should be in the chain."""
        mock_search.return_value = None
        gni.resolve_logo("Test", domain="test.com")
        mock_google.assert_called_once()
        mock_scrape.assert_called_once()
        mock_ddg.assert_called_once()
        mock_search.assert_called_once()
