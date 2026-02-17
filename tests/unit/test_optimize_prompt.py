"""Tests for optimize_prompt() in prompt-optimizer.py."""

import importlib

# Import the module with a hyphen in its name
prompt_optimizer = importlib.import_module("prompt-optimizer")
optimize_prompt = prompt_optimizer.optimize_prompt
TEMPLATES = prompt_optimizer.TEMPLATES
RATIO_HINTS = prompt_optimizer.RATIO_HINTS


class TestOptimizePromptStyles:
    """All four styles should produce valid output."""

    def test_cartoon_produces_output(self):
        result = optimize_prompt("a panda", stijl="cartoon")
        assert isinstance(result, str) and len(result) > 50

    def test_foto_produces_output(self):
        result = optimize_prompt("a panda", stijl="foto")
        assert isinstance(result, str) and len(result) > 50

    def test_logo_produces_output(self):
        result = optimize_prompt("a panda", stijl="logo")
        assert isinstance(result, str) and len(result) > 50

    def test_artistiek_produces_output(self):
        result = optimize_prompt("a panda", stijl="artistiek")
        assert isinstance(result, str) and len(result) > 50

    def test_unknown_style_falls_back_to_cartoon(self):
        result_unknown = optimize_prompt("a panda", stijl="onbekend")
        result_cartoon = optimize_prompt("a panda", stijl="cartoon")
        assert result_unknown == result_cartoon


class TestOptimizePromptTekst:
    """The tekst parameter should only apply for logo style."""

    def test_tekst_included_in_logo_style(self):
        result = optimize_prompt("coffee shop icon", stijl="logo", tekst="Morning Brew")
        assert "Morning Brew" in result

    def test_tekst_ignored_for_non_logo_style(self):
        result = optimize_prompt("a panda", stijl="cartoon", tekst="Some Text")
        assert "Some Text" not in result


class TestOptimizePromptRatio:
    """Ratio hints should be correctly inserted."""

    def test_landscape_ratio_hint(self):
        result = optimize_prompt("test", ratio="16:9")
        assert "Landscape" in result or "widescreen" in result.lower()

    def test_portrait_ratio_hint(self):
        result = optimize_prompt("test", ratio="9:16")
        assert "portrait" in result.lower()

    def test_square_ratio_hint(self):
        result = optimize_prompt("test", ratio="1:1")
        assert "Square" in result


class TestOptimizePromptCleanup:
    """Output should be clean text without double spaces."""

    def test_no_double_spaces_in_output(self):
        for stijl in ["cartoon", "foto", "logo", "artistiek"]:
            result = optimize_prompt("a test subject", stijl=stijl)
            assert "  " not in result, f"Double space found in {stijl} output"
