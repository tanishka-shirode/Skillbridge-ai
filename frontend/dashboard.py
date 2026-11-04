import requests
import streamlit as st
import pandas as pd

from storage import (
    load_data,
    save_profile,
    save_skill_analysis,
    save_workflow,
    save_completed_tasks,
)

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
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 0.25rem;
        overflow-wrap: anywhere;
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
    """Display API data without assuming a fixed response structure."""
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
    """Extract skill names and priority scores from analysis output."""
    if not isinstance(analysis, dict):
        return [], []

    gaps = []
    for key in ["skill_gaps", "missing_skills", "gaps", "skills_to_learn"]:
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


def task_text_from_item(task):
    if isinstance(task, dict):
        return (
            task.get("title")
            or task.get("task")
            or task.get("description")
            or str(task)
        )
    return str(task)


# -------------------- LOAD SAVED DATA --------------------
saved_data = load_data()

if "profile" not in st.session_state:
    st.session_state.profile = saved_data.get("profile")

if "skill_analysis" not in st.session_state:
    st.session_state.skill_analysis = saved_data.get("skill_analysis")

if "workflow" not in st.session_state:
    st.session_state.workflow = saved_data.get("workflow")

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = saved_data.get("completed_tasks", [])

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
st.markdown(
    '<div class="main-title">🎯 SkillBridge AI</div>',
    unsafe_allow_html=True,
)
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
    else:
        skill_names, _ = get_skill_gap_data(analysis or {})
        milestones = workflow.get("milestones", []) if workflow else []
        tasks = workflow.get("learning_tasks", []) if workflow else []
        completed_count = len(st.session_state.completed_tasks)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            show_metric("Target Role", profile.get("target_role", "Not set"))
        with col2:
            show_metric("Current Skills", len(profile.get("current_skills", [])))
        with col3:
            show_metric("Skill Gaps", len(skill_names))
        with col4:
            show_metric("Hours / Week", profile.get("hours_per_week", 0))

        st.divider()

        left, right = st.columns([1.2, 1])

        with left:
            st.subheader("Skill-Gap Analysis")
            if skill_names:
                chart_data = pd.DataFrame(
                    {"Priority": get_skill_gap_data(analysis)[1]},
                    index=skill_names,
                )
                st.bar_chart(chart_data, horizontal=True)
            elif analysis:
                st.info("Analysis completed.")
                with st.expander("View skill analysis"):
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
                st.progress(
                    completed_count / len(tasks) if tasks else 0,
                    text=f"Completed {min(completed_count, len(tasks))} of {len(tasks)} tasks",
                )
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

        experience_options = ["beginner", "intermediate", "advanced"]
        current_level = existing.get("experience_level", "beginner")
        level_index = (
            experience_options.index(current_level)
            if current_level in experience_options
            else 0
        )

        experience_level = st.selectbox(
            "Experience level",
            experience_options,
            index=level_index,
        )

        hours_per_week = st.slider(
            "Hours available per week",
            min_value=1,
            max_value=40,
            value=int(existing.get("hours_per_week", 10)),
        )

        preference_options = [
            "Hands-on projects",
            "Videos",
            "Reading",
            "Practice exercises",
        ]

        learning_preferences = st.multiselect(
            "Preferred learning methods",
            preference_options,
            default=[
                item
                for item in existing.get("learning_preferences", [])
                if item in preference_options
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
                st.session_state.completed_tasks = []

                save_profile(profile)
                save_skill_analysis(result)
                save_workflow({})
                save_completed_tasks([])

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
        st.markdown(f"**Target Role:** {profile.get('target_role', '')}")

        if st.button("Generate Learning Roadmap", type="primary"):
            with st.spinner("Creating your personalized roadmap..."):
                result = post_request(
                    "/api/learning-workflow",
                    profile,
                )

            if result:
                st.session_state.workflow = result
                st.session_state.completed_tasks = []

                save_workflow(result)
                save_completed_tasks([])

                st.success("Your learning roadmap is ready!")

        workflow = st.session_state.workflow

        if workflow:
            roadmap = workflow.get("project_roadmap", {})
            milestones = workflow.get("milestones", [])
            tasks = workflow.get("learning_tasks", [])
            portfolio = workflow.get("portfolio_content", {})

            st.subheader("Recommended Project")

            if isinstance(roadmap, dict):
                st.markdown(
                    f"### {roadmap.get('project_name', 'Project Roadmap')}"
                )
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
                                title = (
                                    milestone.get("title")
                                    or milestone.get("name")
                                    or f"Milestone {index + 1}"
                                )
                                st.markdown(f"**{title}**")
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
                    text = task_text_from_item(task)
                    task_key = f"learning_task_{index}"

                    if task_key not in st.session_state:
                        st.session_state[task_key] = (
                            task_key in st.session_state.completed_tasks
                        )

                    checked = st.checkbox(
                        text,
                        key=task_key,
                    )

                    if checked and task_key not in st.session_state.completed_tasks:
                        st.session_state.completed_tasks.append(task_key)
                        save_completed_tasks(st.session_state.completed_tasks)

                    elif (
                        not checked
                        and task_key in st.session_state.completed_tasks
                    ):
                        st.session_state.completed_tasks.remove(task_key)
                        save_completed_tasks(st.session_state.completed_tasks)

                total_tasks = len(tasks)
                completed_count = sum(
                    1
                    for index in range(total_tasks)
                    if f"learning_task_{index}"
                    in st.session_state.completed_tasks
                )

                st.progress(
                    completed_count / total_tasks if total_tasks else 0,
                    text=f"{completed_count} of {total_tasks} tasks completed",
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