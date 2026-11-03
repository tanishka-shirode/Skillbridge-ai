from Backend.app.agents.project_architect import (
    create_project_milestones as create_milestones
)


def create_milestones_tool(roadmap: dict) -> list[dict]:
    """Create actionable milestones from a project roadmap."""

    return create_milestones(roadmap)