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
    """Prioritize tasks and associate relevant skill gaps."""

    high_priority_keywords = [
        "core", "implement", "develop", "model", "api",
        "machine learning", "rag", "deep learning"
    ]

    # Skill keywords help connect broad skills to relevant project work.
    skill_keywords = {
        "python": ["python", "script", "backend", "implementation"],
        "machine learning": ["model", "machine learning", "training", "prediction"],
        "deep learning": ["model", "neural", "deep learning"],
        "data science": ["data", "analysis", "dataset"],
        "sql": ["database", "sql", "data storage"],
        "api development": ["api", "endpoint", "backend", "integration"],
        "rest api": ["api", "endpoint", "backend", "integration"],
        "git": ["git", "version control", "repository"],
        "testing": ["test", "testing", "validation", "review"],
        "deployment": ["deploy", "deployment", "hosting"],
        "rag": ["rag", "retrieval", "knowledge base", "llm"],
        "llm": ["llm", "language model", "prompt", "rag"],
    }

    for task in tasks:
        title = task.get("title", "").lower()
        milestone = task.get("milestone", "").lower()
        task_text = f"{title} {milestone}"

        if any(keyword in title for keyword in high_priority_keywords):
            task["priority"] = "high"
        elif "planning" in milestone or "setup" in milestone:
            task["priority"] = "high"
        elif "deployment" in milestone or "portfolio" in milestone:
            task["priority"] = "low"
        else:
            task["priority"] = "medium"

        related_gaps = []

        for skill in skill_gaps:
            skill_lower = skill.lower()

            # Direct match in task title or milestone.
            if skill_lower in task_text:
                related_gaps.append(skill)
                continue

            # Match known skill concepts to relevant task wording.
            keywords = skill_keywords.get(skill_lower, [])
            if any(keyword in task_text for keyword in keywords):
                related_gaps.append(skill)

        # Generic implementation tasks can address remaining gaps.
        if not related_gaps and any(
            word in task_text
            for word in ["implement", "develop", "build", "integration"]
        ):
            related_gaps = skill_gaps.copy()

        task["related_skill_gaps"] = related_gaps

    return tasks