from Backend.app.models.schemas import StudentProfile


ROLE_SKILLS = {
    "ai engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Data Processing",
        "LLM Fundamentals",
        "RAG",
        "API Development",
        "Model Evaluation",
        "Git"
    ],
    "machine learning engineer": [
        "Python",
        "Statistics",
        "Machine Learning",
        "Data Processing",
        "Feature Engineering",
        "Model Evaluation",
        "Deep Learning",
        "Model Deployment",
        "Git"
    ],
    "data scientist": [
        "Python",
        "Statistics",
        "SQL",
        "Data Analysis",
        "Data Visualization",
        "Machine Learning",
        "Feature Engineering",
        "Model Evaluation"
    ],
    "software engineer": [
        "Programming",
        "Data Structures",
        "Algorithms",
        "Object-Oriented Programming",
        "Database Fundamentals",
        "API Development",
        "Testing",
        "Git"
    ]
}


SKILL_ALIASES = {
    "basic rag": "RAG",
    "retrieval augmented generation": "RAG",
    "pytorch": "Deep Learning",
    "tensorflow": "Deep Learning",
    "pandas": "Data Processing",
    "numpy": "Data Processing",
    "fastapi": "API Development",
    "flask": "API Development",
    "javascript": "Programming",
    "java": "Programming",
    "c++": "Programming",
    "git and github": "Git",
    "github": "Git",
    "sql": "SQL",
    "mysql": "SQL"
}


def normalize_skill(skill: str) -> str:
    cleaned = skill.strip().lower()
    return SKILL_ALIASES.get(cleaned, skill.strip())


def analyze_skill_gaps(profile: StudentProfile) -> dict:
    target_role = profile.target_role.strip().lower()

    required_skills = ROLE_SKILLS.get(
        target_role,
        ROLE_SKILLS["ai engineer"]
    )

    current_skills = {
        normalize_skill(skill).lower()
        for skill in profile.current_skills
    }

    matched_skills = [
        skill for skill in required_skills
        if skill.lower() in current_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in current_skills
    ]

    return {
        "target_role": profile.target_role,
        "current_skills": profile.current_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "skill_gaps": missing_skills,
        "priority_skills": missing_skills[:5],
        "coverage_percentage": round(
            len(matched_skills) / len(required_skills) * 100
        )
    }