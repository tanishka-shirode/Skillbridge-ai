from mcp.server import MCPServer

from Backend.app.agents.coordinator import coordinate_learning_workflow
from Backend.app.models.schemas import StudentProfile


def register_learning_workflow_tool(mcp: MCPServer):
    @mcp.tool()
    def run_learning_workflow(
        current_skills: list[str],
        target_role: str,
        experience_level: str,
        hours_per_week: int,
        learning_preferences: list[str] | None = None,
    ) -> dict:
        """
        Run the complete SkillBridge AI workflow:
        skill-gap analysis, roadmap, milestones, and prioritized tasks.
        """
        profile = StudentProfile(
            current_skills=current_skills,
            target_role=target_role,
            experience_level=experience_level,
            hours_per_week=hours_per_week,
            learning_preferences=learning_preferences or [],
        )

        return coordinate_learning_workflow(profile)