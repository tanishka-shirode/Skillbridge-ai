# SkillBridge AI

**An AI-powered skill-gap analysis and personalized learning roadmap platform.**

SkillBridge AI helps students identify the skills required for a target role, understand their skill gaps, and follow a structured learning path through projects, tasks, code reviews, and evaluations.

## Features

- **Skill Gap Analysis:** Compare current skills with the skills required for a target role.
- **Personalized Learning Roadmap:** Generate project-based milestones and actionable learning tasks.
- **Multi-Agent Workflow:** Coordinate skill mapping, project planning, task planning, and portfolio generation.
- **Code Review:** Review submitted code using static checks for common issues.
- **Test Evaluation:** Run the project's test suite and report results.
- **Portfolio Suggestions:** Generate portfolio-oriented project content.
- **Interactive Dashboard:** Streamlit interface for profile management, roadmap tracking, code review, and test evaluation.
- **Local Data Persistence:** Save profile and progress data locally so it remains available after refreshing the dashboard.

## Tech Stack

- Python
- FastAPI
- Streamlit
- Pydantic
- Requests
- pytest
- uv

## Architecture

The Streamlit dashboard communicates with the FastAPI backend.

The learning workflow coordinates these modules:

1. **Skill Mapper** – identifies skill gaps.
2. **Project Architect** – proposes projects aligned with target skills.
3. **Task Planner** – breaks projects into manageable learning tasks.
4. **Portfolio Agent** – prepares portfolio-oriented project content.

Additional backend endpoints provide code review and test evaluation.

## Project Structure

```text
SkillBridge-AI/
├── Backend/
│   └── app/
│       └── main.py
├── frontend/
│   ├── dashboard.py
│   ├── app.py
│   ├── storage.py
│   └── .streamlit/
│       └── config.toml
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tanishka-shirode/Skillbridge-ai.git
cd Skillbridge-ai
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Start the backend

Open a terminal in the project root:

```bash
uv run uvicorn Backend.app.main:app --reload
```

Backend API: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

### 4. Start the frontend

Open a second terminal in the project root:

```bash
uv run streamlit run frontend/dashboard.py
```

Streamlit will provide a local URL to open the dashboard in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend welcome/status |
| GET | `/health` | Health check |
| POST | `/api/profile` | Submit student profile |
| POST | `/api/skill-gap` | Analyze skill gaps |
| POST | `/api/learning-workflow` | Generate learning workflow |
| POST | `/api/code-review` | Review submitted code |
| POST | `/api/run-tests` | Run project tests |

## Running Tests

```bash
uv run pytest -q
```

## Data Storage

The current MVP stores dashboard data locally in:

```text
frontend/skillbridge_data.json
```

This file is generated when data is saved. The application does not require a database for its current local-demo workflow.

## Demo Workflow

1. Enter a student profile and target career role.
2. Run skill-gap analysis.
3. Generate the personalized learning workflow.
4. Review milestones and learning tasks.
5. Track completed tasks on the dashboard.
6. Submit code for review.
7. Run the test evaluator and view the results.

## Future Enhancements

- Semantic skill matching using embeddings.
- User authentication and multi-user storage.
- Integration with external learning platforms.
- Deployment with cloud-based persistence.
- More advanced code quality and project evaluation.

---

**SkillBridge AI** — Turning skill gaps into actionable learning paths.
