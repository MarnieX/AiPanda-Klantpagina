"""Tests for API key loading logic in generate_notion_image.py."""

import os
from unittest.mock import patch

import pytest

from generate_notion_image import load_api_key


class TestLoadApiKey:
    """Test the load_api_key() function."""

    def test_returns_existing_env_var_without_dotenv(self):
        """If GEMINI_API_KEY is already set, return it without loading .env."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "env-key-123"}, clear=False):
            with patch("generate_notion_image.load_dotenv") as mock_ld:
                result = load_api_key()
                assert result == "env-key-123"
                mock_ld.assert_not_called()

    def test_exits_when_key_not_found(self):
        """When no key is found in env or .env files, should sys.exit(1)."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("generate_notion_image.load_dotenv"):
                with pytest.raises(SystemExit) as exc_info:
                    load_api_key()
                assert exc_info.value.code == 1

    def test_loads_from_dotenv_when_env_var_missing(self):
        """When GEMINI_API_KEY is not in env, should load from .env file."""
        with patch.dict(os.environ, {}, clear=True):
            def set_key_on_load(path):
                os.environ["GEMINI_API_KEY"] = "from-dotenv"

            with patch("generate_notion_image.load_dotenv", side_effect=set_key_on_load):
                result = load_api_key()
                assert result == "from-dotenv"

        os.environ.pop("GEMINI_API_KEY", None)

    def test_env_var_has_priority(self):
        """Pre-set env var should be returned immediately (Cowork scenario)."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "cowork-key"}, clear=False):
            result = load_api_key()
            assert result == "cowork-key"

    def test_empty_env_var_triggers_dotenv_search(self):
        """An empty string for GEMINI_API_KEY should trigger .env loading."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}, clear=False):
            def set_key_on_load(path):
                os.environ["GEMINI_API_KEY"] = "loaded-key"

            with patch("generate_notion_image.load_dotenv", side_effect=set_key_on_load):
                result = load_api_key()
                assert result == "loaded-key"

        os.environ.pop("GEMINI_API_KEY", None)
