"""Shared fixtures for the AI Panda Klantpagina test suite."""

import sys
from pathlib import Path

import pytest

# Add project root and scripts to sys.path so we can import modules directly
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def project_root():
    """Return the project root directory as a Path."""
    return PROJECT_ROOT


@pytest.fixture
def scripts_dir():
    """Return the scripts directory as a Path."""
    return SCRIPTS_DIR


@pytest.fixture
def sample_company():
    """Return sample company data for testing."""
    return {
        "company_name": "TechCorp",
        "sector": "tech",
        "brand_colors": "#FF5500, #FFFFFF",
        "logo_domain": "techcorp.nl",
    }
