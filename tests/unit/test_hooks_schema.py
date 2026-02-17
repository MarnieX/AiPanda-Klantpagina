"""Tests for plugin/hooks/hooks.json schema validation."""

import json
from pathlib import Path

import pytest


@pytest.fixture
def hooks_data(project_root):
    """Load and parse hooks.json."""
    hooks_path = project_root / "plugin" / "hooks" / "hooks.json"
    assert hooks_path.exists(), f"hooks.json not found at {hooks_path}"
    return json.loads(hooks_path.read_text())


class TestHooksSchema:
    """Validate the structure of hooks.json."""

    def test_valid_json_with_stop_key(self, hooks_data):
        assert "Stop" in hooks_data

    def test_stop_is_a_list(self, hooks_data):
        assert isinstance(hooks_data["Stop"], list)
        assert len(hooks_data["Stop"]) > 0

    def test_each_entry_has_hooks_list(self, hooks_data):
        for entry in hooks_data["Stop"]:
            assert "hooks" in entry
            assert isinstance(entry["hooks"], list)

    def test_each_hook_has_required_fields(self, hooks_data):
        for entry in hooks_data["Stop"]:
            for hook in entry["hooks"]:
                assert "type" in hook, "Hook missing 'type' field"
                assert "prompt" in hook, "Hook missing 'prompt' field"
                assert "timeout" in hook, "Hook missing 'timeout' field"

    def test_timeout_is_reasonable(self, hooks_data):
        for entry in hooks_data["Stop"]:
            for hook in entry["hooks"]:
                timeout = hook["timeout"]
                assert isinstance(timeout, (int, float))
                assert 1 <= timeout <= 120, f"Timeout {timeout}s outside reasonable range (1-120s)"
