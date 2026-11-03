from mcp.server import MCPServer

from Backend.app.mcp_servers.task_planner_tools.generate_learning_tasks import (
    generate_learning_tasks_tool
)
from Backend.app.mcp_servers.task_planner_tools.prioritize_tasks import (
    prioritize_tasks_tool
)

mcp = MCPServer("SkillBridge Task Planner")


@mcp.tool()
def generate_learning_tasks(
    milestones: list[dict]
) -> list[dict]:
    """Break project milestones into actionable learning tasks."""
    return generate_learning_tasks_tool(milestones)


@mcp.tool()
def prioritize_tasks(
    tasks: list[dict],
    skill_gaps: list[str]
) -> list[dict]:
    """Assign priorities and link tasks to skill gaps."""
    return prioritize_tasks_tool(tasks, skill_gaps)


if __name__ == "__main__":
    mcp.run(transport="stdio")