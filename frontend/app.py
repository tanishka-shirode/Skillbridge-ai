import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 SkillBridge AI")
st.caption("Your AI-powered personalized learning companion")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Student Profile",
        "Learning Roadmap",
        "Code Review",
        "Test Evaluation",
    ],
)

def post_request(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure FastAPI is running.")
    except requests.exceptions.HTTPError:
        st.error(f"API error: {response.status_code}")
        st.code(response.text)
    except requests.exceptions.RequestException as error:
        st.error(f"Request failed: {error}")
    return None


if page == "Student Profile":
    st.header("Create Your Student Profile")

    with st.form("profile_form"):
        skills = st.text_input(
            "Current skills",
            placeholder="Python, HTML, CSS",
        )
        target_role = st.text_input(
            "Target role",
            placeholder="AI Engineer",
        )
        experience_level = st.selectbox(
            "Experience level",
            ["beginner", "intermediate", "advanced"],
        )
        hours_per_week = st.slider(
            "Hours available per week",
            1,
            40,
            10,
        )
        learning_preferences = st.multiselect(
            "Preferred learning methods",
            [
                "Hands-on projects",
                "Videos",
                "Reading",
                "Practice exercises",
            ],
        )

        submitted = st.form_submit_button(
            "Analyze My Skills",
            type="primary",
        )

    if submitted:
        profile = {
            "current_skills": [
                skill.strip()
                for skill in skills.split(",")
                if skill.strip()
            ],
            "target_role": target_role,
            "experience_level": experience_level,
            "hours_per_week": hours_per_week,
            "learning_preferences": learning_preferences,
        }

        if not profile["current_skills"] or not target_role.strip():
            st.warning("Please enter your current skills and target role.")
        else:
            with st.spinner("Analyzing your skills..."):
                result = post_request("/api/skill-gap", profile)

            if result:
                st.session_state["profile"] = profile
                st.session_state["skill_analysis"] = result
                st.success("Skill-gap analysis completed!")
                st.subheader("Your Skill-Gap Analysis")
                st.json(result)


elif page == "Learning Roadmap":
    st.header("Personalized Learning Roadmap")

    profile = st.session_state.get("profile")

    if not profile:
        st.info("Create and analyze your student profile first.")
    else:
        st.write(f"**Target role:** {profile['target_role']}")

        if st.button("Generate Learning Roadmap", type="primary"):
            with st.spinner("Building your personalized learning plan..."):
                result = post_request(
                    "/api/learning-workflow",
                    profile,
                )

            if result:
                st.session_state["learning_workflow"] = result
                st.success("Learning roadmap generated!")

        result = st.session_state.get("learning_workflow")

        if result:
            st.subheader("Project Roadmap")
            st.json(result.get("project_roadmap", {}))

            st.subheader("Milestones")
            st.json(result.get("milestones", []))

            st.subheader("Learning Tasks")
            st.json(result.get("learning_tasks", []))

            st.subheader("Portfolio Content")
            st.json(result.get("portfolio_content", {}))


elif page == "Code Review":
    st.header("AI Code Review")
    st.write("Submit code to check for common issues.")

    language = st.selectbox(
        "Programming language",
        ["python", "javascript", "java", "cpp"],
    )
    code = st.text_area(
        "Paste your code",
        height=300,
        placeholder="Paste your code here...",
    )

    if st.button("Review Code", type="primary"):
        if not code.strip():
            st.warning("Please paste some code first.")
        else:
            with st.spinner("Reviewing your code..."):
                result = post_request(
                    "/api/code-review",
                    {
                        "code": code,
                        "language": language,
                    },
                )

            if result:
                st.subheader("Review Results")
                st.json(result)


elif page == "Test Evaluation":
    st.header("Project Test Evaluation")
    st.write("Run the project's automated tests through the backend.")

    timeout_seconds = st.slider(
        "Test timeout (seconds)",
        min_value=5,
        max_value=120,
        value=60,
    )

    if st.button("Run Tests", type="primary"):
        with st.spinner("Running tests..."):
            result = post_request(
                "/api/run-tests",
                {"timeout_seconds": timeout_seconds},
            )

        if result:
            status = result.get("status", "unknown")

            if status == "passed":
                st.success("All tests passed!")
            else:
                st.warning(f"Test status: {status}")

            st.json(result)