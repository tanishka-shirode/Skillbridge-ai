PROJECT_TEMPLATES = {
    "AI Engineer": {
        "name": "AI Skill Gap Analyzer",
        "description": (
            "A web application that analyzes a learner's skills against "
            "an AI Engineer role and recommends a personalized learning path."
        ),
        "skills": [
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
        "tech_stack": [
            "Python",
            "FastAPI",
            "Scikit-learn",
            "Streamlit",
            "Git"
        ]
    },
    "Machine Learning Engineer": {
        "name": "ML Model Training and Evaluation Platform",
        "description": (
            "A platform to train machine learning models, evaluate their "
            "performance, and compare experiments."
        ),
        "skills": [
            "Python",
            "Statistics",
            "Machine Learning",
            "Data Processing",
            "Feature Engineering",
            "Model Evaluation",
            "Model Deployment",
            "Git"
        ],
        "tech_stack": [
            "Python",
            "Pandas",
            "Scikit-learn",
            "FastAPI",
            "Streamlit",
            "Git"
        ]
    },
    "Data Scientist": {
        "name": "Exploratory Data Analysis Dashboard",
        "description": (
            "An interactive dashboard that explores datasets, visualizes "
            "patterns, and presents useful data insights."
        ),
        "skills": [
            "Python",
            "Statistics",
            "SQL",
            "Data Analysis",
            "Data Visualization",
            "Machine Learning",
            "Feature Engineering"
        ],
        "tech_stack": [
            "Python",
            "Pandas",
            "NumPy",
            "Matplotlib",
            "Plotly",
            "Streamlit",
            "SQL"
        ]
    },
    "Software Engineer": {
        "name": "Task Management REST API",
        "description": (
            "A REST API for managing tasks, users, and task status "
            "with validation and automated tests."
        ),
        "skills": [
            "Programming",
            "Data Structures",
            "Algorithms",
            "Object-Oriented Programming",
            "Database Fundamentals",
            "API Development",
            "Testing",
            "Git"
        ],
        "tech_stack": [
            "Python",
            "FastAPI",
            "SQLite",
            "Pytest",
            "Git"
        ]
    }
}


def generate_project_roadmap(
    target_role: str,
    skill_gaps: list[str]
) -> dict:
    """Generate a role-aligned project roadmap."""

    role = target_role.strip().lower()

    template = next(
        (
            value for key, value in PROJECT_TEMPLATES.items()
            if key.lower() == role
        ),
        PROJECT_TEMPLATES["AI Engineer"]
    )

    relevant_skills = [
        skill for skill in template["skills"]
        if skill.lower() in {gap.lower() for gap in skill_gaps}
    ]

    return {
        "target_role": target_role,
        "project_name": template["name"],
        "description": template["description"],
        "skills_to_practice": relevant_skills or template["skills"][:5],
        "tech_stack": template["tech_stack"],
        "roadmap": [
            {
                "phase": 1,
                "title": "Planning and Setup",
                "tasks": [
                    "Define project requirements",
                    "Create the project repository",
                    "Set up the development environment"
                ]
            },
            {
                "phase": 2,
                "title": "Core Development",
                "tasks": [
                    "Implement the main features",
                    "Apply the selected technical skills",
                    "Test each component"
                ]
            },
            {
                "phase": 3,
                "title": "Integration and Testing",
                "tasks": [
                    "Integrate all components",
                    "Test expected and edge-case inputs",
                    "Fix identified issues"
                ]
            },
            {
                "phase": 4,
                "title": "Deployment and Portfolio",
                "tasks": [
                    "Prepare project documentation",
                    "Deploy or demonstrate the application",
                    "Add screenshots and usage instructions to README"
                ]
            }
        ]
    }


def create_project_milestones(roadmap: dict) -> list[dict]:
    """Convert a project roadmap into actionable milestones."""

    milestones = []

    for phase in roadmap.get("roadmap", []):
        milestones.append({
            "milestone": phase["phase"],
            "title": phase["title"],
            "tasks": phase["tasks"],
            "deliverable": (
                f"Completed output for: {phase['title']}"
            )
        })

    return milestones