import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from Backend.app.agents.skill_mapper import ROLE_SKILLS


def test_role_skills_are_available():
    assert ROLE_SKILLS


def test_ai_engineer_role_exists():
    assert "ai engineer" in ROLE_SKILLS