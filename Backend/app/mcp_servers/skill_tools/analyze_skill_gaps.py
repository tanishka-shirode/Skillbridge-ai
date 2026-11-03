from Backend.app.models.schemas import StudentProfile
from Backend.app.agents.skill_mapper import analyze_skill_gaps


def analyze_gaps(
    current_skills: list[str],
    target_role: str,
    experience_level: str,
    hours_per_week: int,
    learning_preferences: list[str] | None = None
) -> dict:
    """Analyze a learner's skills and identify gaps for a target role."""

    profile = StudentProfile(
        current_skills=current_skills,
        target_role=target_role,
        experience_level=experience_level,
        hours_per_week=hours_per_week,
        learning_preferences=learning_preferences or []
    )

    return analyze_skill_gaps(profile)