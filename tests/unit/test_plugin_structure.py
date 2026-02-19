"""Tests for current plugin structure after hooks removal."""

from pathlib import Path


def test_hooks_directory_removed(project_root):
    hooks_dir = project_root / "plugin" / "hooks"
    assert not hooks_dir.exists()


def test_panda_server_exists(project_root):
    server_path = project_root / "plugin" / "servers" / "panda-server.py"
    assert server_path.exists()


def test_deprecated_server_removed(project_root):
    old_server = project_root / "plugin" / "servers" / "gemini-image-server.py"
    assert not old_server.exists()
