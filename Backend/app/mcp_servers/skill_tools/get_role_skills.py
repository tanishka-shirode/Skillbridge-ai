from Backend.app.agents.skill_mapper import ROLE_SKILLS


def get_role_skills(target_role: str) -> dict:
    """Get the required skills for a target job role."""

    role = target_role.strip().lower()

    if role not in ROLE_SKILLS:
        return {
            "target_role": target_role,
            "error": "Role not found",
            "available_roles": list(ROLE_SKILLS.keys())
        }

    return {
        "target_role": target_role,
        "required_skills": ROLE_SKILLS[role]
    }