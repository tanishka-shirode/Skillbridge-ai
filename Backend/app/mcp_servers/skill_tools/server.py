from mcp.server import MCPServer

from Backend.app.mcp_servers.skill_tools.get_role_skills import (
    get_role_skills
)
from Backend.app.mcp_servers.skill_tools.analyze_skill_gaps import (
    analyze_gaps
)

mcp = MCPServer("SkillBridge Skill Mapper")


@mcp.tool()
def get_role_skills_tool(target_role: str) -> dict:
    """Return the required skills for a target job role."""
    return get_role_skills(target_role)


@mcp.tool()
def analyze_skill_gaps_tool(
    current_skills: list[str],
    target_role: str,
    experience_level: str,
    hours_per_week: int,
    learning_preferences: list[str] | None = None
) -> dict:
    """Compare current skills with role requirements and return skill gaps."""
    return analyze_gaps(
        current_skills=current_skills,
        target_role=target_role,
        experience_level=experience_level,
        hours_per_week=hours_per_week,
        learning_preferences=learning_preferences
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")