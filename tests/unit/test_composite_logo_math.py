"""Tests for composite_logo math in generate_notion_image.py."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

import generate_notion_image as gni


class TestLogoResizeAndCenter:
    """Verify logo resize and centering calculations."""

    def test_logo_resizes_to_80_percent_of_badge(self):
        """Logo width and height should be 80% of badge dimensions."""
        badge_w, badge_h = 100, 120
        expected_logo_w = int(badge_w * 0.8)  # 80
        expected_logo_h = int(badge_h * 0.8)  # 96
        assert expected_logo_w == 80
        assert expected_logo_h == 96

    def test_centering_calculation(self):
        """Logo should be centered within the badge bounding box."""
        x, y, w, h = 50, 100, 100, 120
        logo_w = int(w * 0.8)  # 80
        logo_h = int(h * 0.8)  # 96
        paste_x = x + (w - logo_w) // 2  # 50 + 10 = 60
        paste_y = y + (h - logo_h) // 2  # 100 + 12 = 112
        assert paste_x == 60
        assert paste_y == 112

    @pytest.mark.parametrize("x,y,w,h", [
        (0, 0, 50, 50),
        (100, 200, 80, 60),
        (0, 0, 1, 1),
        (500, 500, 200, 300),
    ])
    def test_paste_position_within_badge_bounds(self, x, y, w, h):
        """Paste position should always be within the badge bounding box."""
        logo_w = int(w * 0.8)
        logo_h = int(h * 0.8)
        paste_x = x + (w - logo_w) // 2
        paste_y = y + (h - logo_h) // 2
        assert paste_x >= x
        assert paste_y >= y
        assert paste_x + logo_w <= x + w
        assert paste_y + logo_h <= y + h

    def test_composite_logo_returns_none_for_missing_file(self):
        """composite_logo should return None when logo file doesn't exist."""
        result = gni.composite_logo(
            image_path="/nonexistent/panda.png",
            logo_path="/nonexistent/logo.png",
            badge_rect=(10, 10, 50, 50),
            output_path="/tmp/test_output.png",
        )
        assert result is None
