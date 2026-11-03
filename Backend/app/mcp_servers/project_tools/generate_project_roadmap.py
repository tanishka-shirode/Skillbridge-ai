from Backend.app.agents.project_architect import (
    generate_project_roadmap as generate_roadmap
)


def generate_roadmap_tool(
    target_role: str,
    skill_gaps: list[str]
) -> dict:
    """Generate a practical project roadmap based on a learner's skill gaps."""

    return generate_roadmap(
        target_role=target_role,
        skill_gaps=skill_gaps
    )