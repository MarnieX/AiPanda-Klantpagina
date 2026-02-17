"""Tests for build_client_prompt() and SECTOR_BACKGROUNDS in generate_notion_image.py."""

import generate_notion_image as gni


class TestSectorBackgrounds:
    """Verify SECTOR_BACKGROUNDS dictionary completeness and content."""

    EXPECTED_SECTORS = [
        "telecom", "retail", "e-commerce", "finance", "zorg",
        "logistiek", "tech", "onderwijs", "energie", "overheid",
        "food", "horeca", "bakkerij",
    ]

    def test_all_expected_sectors_present(self):
        for sector in self.EXPECTED_SECTORS:
            assert sector in gni.SECTOR_BACKGROUNDS, f"Missing sector: {sector}"

    def test_total_sector_count(self):
        assert len(gni.SECTOR_BACKGROUNDS) == 13

    def test_all_values_are_nonempty_strings(self):
        for sector, bg in gni.SECTOR_BACKGROUNDS.items():
            assert isinstance(bg, str) and len(bg) > 10, f"Empty/short background for {sector}"

    def test_food_and_horeca_are_identical(self):
        """Document known duplicate: food and horeca share the same background."""
        assert gni.SECTOR_BACKGROUNDS["food"] == gni.SECTOR_BACKGROUNDS["horeca"]


class TestBuildClientPrompt:
    """Test the prompt building logic."""

    def test_known_sector_uses_correct_background(self):
        prompt = gni.build_client_prompt("TestBV", sector="telecom")
        assert "telecom operations center" in prompt

    def test_unknown_sector_falls_back_to_tech(self):
        prompt = gni.build_client_prompt("TestBV", sector="onbekend")
        assert gni.SECTOR_BACKGROUNDS["tech"] in prompt

    def test_none_sector_falls_back_to_tech(self):
        prompt = gni.build_client_prompt("TestBV", sector=None)
        assert gni.SECTOR_BACKGROUNDS["tech"] in prompt

    def test_sector_is_case_insensitive(self):
        prompt_lower = gni.build_client_prompt("X", sector="telecom")
        prompt_upper = gni.build_client_prompt("X", sector="TELECOM")
        prompt_mixed = gni.build_client_prompt("X", sector="Telecom")
        assert prompt_lower == prompt_upper == prompt_mixed

    def test_company_name_appears_in_prompt(self):
        prompt = gni.build_client_prompt("Acme Corp")
        assert "Acme Corp" in prompt

    def test_brand_colors_included_when_provided(self):
        prompt = gni.build_client_prompt("X", brand_colors="#FF0000, #00FF00")
        assert "#FF0000" in prompt
        assert "#00FF00" in prompt

    def test_brand_colors_trimmed(self):
        prompt = gni.build_client_prompt("X", brand_colors="  #AAA  ,  #BBB  ")
        assert "#AAA" in prompt
        assert "#BBB" in prompt
        assert "  #AAA  " not in prompt

    def test_no_brand_colors_omits_color_instruction(self):
        prompt = gni.build_client_prompt("X", brand_colors=None)
        assert "accent colors matching the company brand" not in prompt

    def test_has_logo_true_includes_logo_instruction(self):
        prompt = gni.build_client_prompt("X", has_logo=True)
        assert "company logo" in prompt.lower()

    def test_has_logo_false_omits_logo_instruction(self):
        prompt = gni.build_client_prompt("X", has_logo=False)
        assert "company logo" not in prompt.lower()

    def test_prompt_is_nonempty_string(self):
        prompt = gni.build_client_prompt("TestBV")
        assert isinstance(prompt, str) and len(prompt) > 100

    def test_prompt_mentions_panda(self):
        prompt = gni.build_client_prompt("TestBV")
        assert "panda" in prompt.lower()

    def test_prompt_mentions_whiteboard(self):
        prompt = gni.build_client_prompt("TestBV")
        assert "whiteboard" in prompt.lower()
