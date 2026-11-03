def generate_learning_tasks(milestones: list[dict]) -> list[dict]:
    """Convert milestones into actionable learning tasks."""

    tasks = []
    task_id = 1

    for milestone in milestones:
        milestone_title = milestone.get("title", "Project Milestone")

        for task_name in milestone.get("tasks", []):
            tasks.append({
                "task_id": task_id,
                "milestone": milestone_title,
                "title": task_name,
                "description": (
                    f"Complete '{task_name}' as part of "
                    f"the {milestone_title} milestone."
                ),
                "priority": "medium",
                "estimated_hours": 2,
                "completion_criteria": (
                    f"'{task_name}' is completed and verified."
                )
            })
            task_id += 1

    return tasks


def prioritize_tasks(tasks: list[dict], skill_gaps: list[str]) -> list[dict]:
    """Prioritize tasks using task order and skill gap relevance."""

    high_priority_keywords = [
        "core", "implement", "develop", "model", "api",
        "machine learning", "rag", "deep learning"
    ]

    for task in tasks:
        title = task.get("title", "").lower()
        milestone = task.get("milestone", "").lower()

        if any(keyword in title for keyword in high_priority_keywords):
            task["priority"] = "high"
        elif "planning" in milestone or "setup" in milestone:
            task["priority"] = "high"
        elif "deployment" in milestone or "portfolio" in milestone:
            task["priority"] = "low"
        else:
            task["priority"] = "medium"

        task["related_skill_gaps"] = [
            skill for skill in skill_gaps
            if skill.lower() in title
        ]

    return tasks