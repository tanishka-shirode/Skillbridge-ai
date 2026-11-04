import requests
import streamlit as st
import pandas as pd

# -------------------- CONFIG --------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- STYLING --------------------
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        color: #9CA3AF;
        margin-top: 0.25rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #1A1D29;
        border: 1px solid #303443;
        padding: 1rem;
        border-radius: 12px;
        min-height: 110px;
    }
    .metric-label {
        color: #A1A1AA;
        font-size: 0.9rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    .section-note {
        color: #9CA3AF;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HELPERS --------------------
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
        st.error("Backend is not running. Start FastAPI in another terminal.")
    except requests.exceptions.HTTPError:
        st.error(f"API error: {response.status_code}")
        st.code(response.text)
    except requests.exceptions.RequestException as error:
        st.error(f"Request failed: {error}")

    return None


def show_metric(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_data(data):
    """Display API output safely, regardless of its structure."""
    if isinstance(data, dict):
        for key, value in data.items():
            st.markdown(f"**{key.replace('_', ' ').title()}**")
            if isinstance(value, (dict, list)):
                display_data(value)
            else:
                st.write(value)

    elif isinstance(data, list):
        if not data:
            st.caption("No items available.")
        for index, item in enumerate(data, start=1):
            with st.container(border=True):
                st.markdown(f"**Item {index}**")
                display_data(item)

    else:
        st.write(data)


def get_skill_gap_data(analysis):
    """Extract skill names and scores from common API response shapes."""
    if not isinstance(analysis, dict):
        return [], []

    possible_keys = [
        "skill_gaps",
        "missing_skills",
        "gaps",
        "skills_to_learn",
    ]

    gaps = []
    for key in possible_keys:
        value = analysis.get(key)
        if isinstance(value, list):
            gaps = value
            break

    names = []
    scores = []

    for item in gaps:
        if isinstance(item, str):
            names.append(item)
            scores.append(1)
        elif isinstance(item, dict):
            name = (
                item.get("skill")
                or item.get("name")
                or item.get("skill_name")
                or item.get("title")
            )
            score = (
                item.get("priority_score")
                or item.get("priority")
                or item.get("score")
                or 1
            )
            if name:
                names.append(str(name))
                try:
                    scores.append(float(score))
                except (TypeError, ValueError):
                    scores.append(1)

    return names, scores


# -------------------- SESSION STATE --------------------
if "profile" not in st.session_state:
    st.session_state.profile = None

if "skill_analysis" not in st.session_state:
    st.session_state.skill_analysis = None

if "workflow" not in st.session_state:
    st.session_state.workflow = None

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## 🎯 SkillBridge AI")
    st.caption("Personalized AI learning companion")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Student Profile",
            "Learning Roadmap",
            "Code Review",
            "Test Evaluation",
        ],
    )

    st.divider()
    st.caption("Powered by FastAPI + Streamlit")

# -------------------- HEADER --------------------
st.markdown('<div class="main-title">🎯 SkillBridge AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Build skills. Follow your roadmap. Track your progress.</div>',
    unsafe_allow_html=True,
)

# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    st.header("Dashboard Overview")

    profile = st.session_state.profile
    analysis = st.session_state.skill_analysis
    workflow = st.session_state.workflow

    if not profile:
        st.info("Start by creating your student profile.")
        if st.button("Create Student Profile", type="primary"):
            st.session_state["navigate_to_profile"] = True
            st.rerun()

    else:
        skill_names, skill_scores = get_skill_gap_data(analysis or {})
        milestones = workflow.get("milestones", []) if workflow else []
        tasks = workflow.get("learning_tasks", []) if workflow else []

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            show_metric("Target Role", profile["target_role"])
        with col2:
            show_metric("Current Skills", len(profile["current_skills"]))
        with col3:
            show_metric("Skill Gaps", len(skill_names))
        with col4:
            show_metric("Hours / Week", profile["hours_per_week"])

        st.divider()

        left, right = st.columns([1.2, 1])

        with left:
            st.subheader("Your Skill-Gap Analysis")
            if skill_names:
                chart_data = pd.DataFrame(
                    {"Priority": skill_scores},
                    index=skill_names,
                )
                st.bar_chart(chart_data, horizontal=True)
            elif analysis:
                st.info("Analysis completed. See details below.")
                with st.expander("View full skill analysis"):
                    display_data(analysis)
            else:
                st.info("Analyze your profile to view skill gaps.")

        with right:
            st.subheader("Learning Plan")
            if workflow:
                roadmap = workflow.get("project_roadmap", {})
                if isinstance(roadmap, dict):
                    st.markdown(
                        f"**{roadmap.get('project_name', 'Your Project')}**"
                    )
                    st.write(roadmap.get("description", ""))
                else:
                    display_data(roadmap)

                st.metric("Milestones", len(milestones))
                st.metric("Learning Tasks", len(tasks))
            else:
                st.info("Generate your roadmap from the Learning Roadmap page.")

        if analysis:
            with st.expander("View complete skill analysis"):
                display_data(analysis)

# -------------------- STUDENT PROFILE --------------------
elif page == "Student Profile":
    st.header("Create Your Student Profile")
    st.write("Tell us about your current skills and learning goals.")

    existing = st.session_state.profile or {}

    with st.form("profile_form"):
        skills = st.text_input(
            "Current skills",
            value=", ".join(existing.get("current_skills", [])),
            placeholder="Python, HTML, CSS",
        )

        target_role = st.text_input(
            "Target role",
            value=existing.get("target_role", ""),
            placeholder="AI Engineer",
        )

        experience_level = st.selectbox(
            "Experience level",
            ["beginner", "intermediate", "advanced"],
            index=["beginner", "intermediate", "advanced"].index(
                existing.get("experience_level", "beginner")
            ),
        )

        hours_per_week = st.slider(
            "Hours available per week",
            min_value=1,
            max_value=40,
            value=existing.get("hours_per_week", 10),
        )

        learning_preferences = st.multiselect(
            "Preferred learning methods",
            [
                "Hands-on projects",
                "Videos",
                "Reading",
                "Practice exercises",
            ],
            default=existing.get("learning_preferences", []),
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
            "target_role": target_role.strip(),
            "experience_level": experience_level,
            "hours_per_week": hours_per_week,
            "learning_preferences": learning_preferences,
        }

        if not profile["current_skills"] or not profile["target_role"]:
            st.warning("Please enter your current skills and target role.")
        else:
            with st.spinner("Analyzing your skills..."):
                result = post_request("/api/skill-gap", profile)

            if result:
                st.session_state.profile = profile
                st.session_state.skill_analysis = result
                st.session_state.workflow = None
                st.success("Skill-gap analysis completed!")
                st.subheader("Analysis Results")
                display_data(result)

# -------------------- LEARNING ROADMAP --------------------
elif page == "Learning Roadmap":
    st.header("Personalized Learning Roadmap")

    profile = st.session_state.profile

    if not profile:
        st.info("Create your student profile first.")
    else:
        st.markdown(f"**Target Role:** {profile['target_role']}")

        if st.button("Generate Learning Roadmap", type="primary"):
            with st.spinner("Creating your personalized roadmap..."):
                result = post_request(
                    "/api/learning-workflow",
                    profile,
                )

            if result:
                st.session_state.workflow = result
                st.success("Your learning roadmap is ready!")

        workflow = st.session_state.workflow

        if workflow:
            roadmap = workflow.get("project_roadmap", {})
            milestones = workflow.get("milestones", [])
            tasks = workflow.get("learning_tasks", [])
            portfolio = workflow.get("portfolio_content", {})

            st.subheader("Recommended Project")
            if isinstance(roadmap, dict):
                st.markdown(f"### {roadmap.get('project_name', 'Project Roadmap')}")
                st.write(roadmap.get("description", ""))

                tech_stack = roadmap.get("tech_stack", [])
                if tech_stack:
                    st.markdown("**Tech Stack**")
                    st.write(" · ".join(map(str, tech_stack)))

                features = roadmap.get("skills_to_practice", [])
                if features:
                    st.markdown("**Skills to Practice**")
                    st.write(" · ".join(map(str, features)))
            else:
                display_data(roadmap)

            st.subheader("Milestones")
            if milestones:
                cols = st.columns(2)
                for index, milestone in enumerate(milestones):
                    with cols[index % 2]:
                        with st.container(border=True):
                            if isinstance(milestone, dict):
                                st.markdown(
                                    f"**{milestone.get('title', milestone.get('name', f'Milestone {index + 1}'))}**"
                                )
                                display_data({
                                    key: value
                                    for key, value in milestone.items()
                                    if key not in ["title", "name"]
                                })
                            else:
                                st.markdown(f"**Milestone {index + 1}**")
                                st.write(milestone)
            else:
                st.info("No milestones returned.")

            st.subheader("Learning Tasks")
            if tasks:
                for index, task in enumerate(tasks):
                    task_text = (
                        task.get("title")
                        or task.get("task")
                        or task.get("description")
                        or str(task)
                    ) if isinstance(task, dict) else str(task)

                    st.checkbox(
                        task_text,
                        key=f"learning_task_{index}",
                    )
            else:
                st.info("No learning tasks returned.")

            st.subheader("Portfolio Content")
            with st.expander("View generated portfolio content"):
                display_data(portfolio)

# -------------------- CODE REVIEW --------------------
elif page == "Code Review":
    st.header("Code Review")
    st.caption("Check your code for common issues.")

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
            st.warning("Please paste your code first.")
        else:
            with st.spinner("Reviewing code..."):
                result = post_request(
                    "/api/code-review",
                    {"code": code, "language": language},
                )

            if result:
                st.subheader("Review Results")
                display_data(result)

# -------------------- TEST EVALUATION --------------------
elif page == "Test Evaluation":
    st.header("Test Evaluation")
    st.write("Run the project's automated test suite.")

    timeout_seconds = st.slider(
        "Timeout (seconds)",
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
            elif status == "failed":
                st.error("Some tests failed.")
            else:
                st.warning(f"Test status: {status}")

            st.subheader("Test Output")
            if result.get("stdout"):
                st.code(result["stdout"])
            if result.get("stderr"):
                st.code(result["stderr"])

            with st.expander("Full test response"):
                display_data(result)