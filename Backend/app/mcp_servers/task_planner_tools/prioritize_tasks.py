from Backend.app.agents.task_planner import (
    prioritize_tasks as prioritize
)


def prioritize_tasks_tool(
    tasks: list[dict],
    skill_gaps: list[str]
) -> list[dict]:
    """Assign task priorities and identify related skill gaps."""

    return prioritize(tasks, skill_gaps)