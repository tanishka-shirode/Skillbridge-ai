from mcp.server import MCPServer

from Backend.app.mcp_servers.project_tools.generate_project_roadmap import (
    generate_roadmap_tool
)
from Backend.app.mcp_servers.project_tools.create_project_milestones import (
    create_milestones_tool
)

mcp = MCPServer("SkillBridge Project Architect")


@mcp.tool()
def generate_project_roadmap_tool(
    target_role: str,
    skill_gaps: list[str]
) -> dict:
    """Generate a role-aligned project roadmap."""
    return generate_roadmap_tool(target_role, skill_gaps)


@mcp.tool()
def create_project_milestones_tool(roadmap: dict) -> list[dict]:
    """Create ordered milestones from a project roadmap."""
    return create_milestones_tool(roadmap)


if __name__ == "__main__":
    mcp.run(transport="stdio")