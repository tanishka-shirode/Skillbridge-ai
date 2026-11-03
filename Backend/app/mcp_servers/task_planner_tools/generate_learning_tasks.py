from Backend.app.agents.task_planner import (
    generate_learning_tasks as generate_tasks
)


def generate_learning_tasks_tool(milestones: list[dict]) -> list[dict]:
    """Generate actionable learning tasks from project milestones."""

    return generate_tasks(milestones)