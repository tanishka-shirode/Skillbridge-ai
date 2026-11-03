from Backend.app.agents.skill_mapper import analyze_skill_gaps
from Backend.app.agents.project_architect import (
    generate_project_roadmap,
    create_project_milestones,
)
from Backend.app.agents.task_planner import (
    generate_learning_tasks,
    prioritize_tasks,
)


def coordinate_learning_workflow(profile) -> dict:
    """Coordinate the SkillBridge AI learning workflow."""

    # 1. Analyze skill gaps
    skill_analysis = analyze_skill_gaps(profile)
    skill_gaps = skill_analysis.get("skill_gaps", [])

    # 2. Generate roadmap using role and skill gaps
    roadmap = generate_project_roadmap(
        profile.target_role,
        skill_gaps,
    )

    # 3. Create milestones
    milestones = create_project_milestones(roadmap)

    # 4. Generate and prioritize learning tasks
    tasks = generate_learning_tasks(milestones)
    prioritized_tasks = prioritize_tasks(tasks, skill_gaps)

    return {
        "status": "success",
        "target_role": profile.target_role,
        "skill_analysis": skill_analysis,
        "project_roadmap": roadmap,
        "milestones": milestones,
        "learning_tasks": prioritized_tasks,
    }