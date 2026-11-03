def generate_portfolio_content(
    project_name: str,
    project_description: str,
    technologies: list[str],
    features: list[str],
    role: str = "Developer",
) -> dict:
    """Generate portfolio-ready content from project details."""

    project_name = project_name.strip()
    project_description = project_description.strip()
    technologies = [item.strip() for item in technologies if item.strip()]
    features = [item.strip() for item in features if item.strip()]

    if not project_name or not project_description:
        return {
            "status": "error",
            "message": "Project name and description are required."
        }

    tech_text = ", ".join(technologies) if technologies else "Not specified"
    feature_list = "\n".join(f"- {feature}" for feature in features)
    if not feature_list:
        feature_list = "- Add project features here"

    summary = (
        f"{project_name} is a project focused on {project_description} "
        f"It was developed using {tech_text}."
    )

    readme = f"""# {project_name}

## Overview
{project_description}

## Technologies Used
{tech_text}

## Key Features
{feature_list}

## Role
{role}

## Getting Started
1. Clone this repository.
2. Install the required dependencies.
3. Configure any required environment variables.
4. Run the application using the project instructions.
"""

    resume_bullets = [
        f"Developed {project_name} using {tech_text}.",
        f"Implemented key features including: {', '.join(features[:3])}."
        if features
        else f"Worked on the core functionality of {project_name}.",
        f"Applied {tech_text} to build a solution for {project_description}."
    ]

    return {
        "status": "success",
        "project_name": project_name,
        "summary": summary,
        "readme_content": readme,
        "resume_bullets": resume_bullets,
        "skills_demonstrated": technologies,
        "features": features,
    }