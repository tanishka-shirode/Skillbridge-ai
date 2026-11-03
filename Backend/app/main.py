from fastapi import FastAPI
from pydantic import BaseModel, Field

from Backend.app.models.schemas import StudentProfile
from Backend.app.agents.skill_mapper import analyze_skill_gaps
from Backend.app.agents.coordinator import coordinate_learning_workflow
from Backend.app.agents.code_reviewer import review_code
from Backend.app.agents.evaluator import run_tests


app = FastAPI(
    title="SkillBridge AI",
    description="Multi-agent AI learning and project guidance system",
    version="0.6.0"
)


class CodeReviewRequest(BaseModel):
    code: str = Field(min_length=1)
    language: str = "python"


class TestEvaluationRequest(BaseModel):
    timeout_seconds: int = Field(default=60, ge=5, le=120)


@app.get("/")
def home():
    return {
        "message": "Welcome to SkillBridge AI",
        "version": "0.6.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/profile")
def create_profile(profile: StudentProfile):
    return {
        "message": "Student profile received successfully",
        "profile": profile.model_dump()
    }


@app.post("/api/skill-gap")
def skill_gap_analysis(profile: StudentProfile):
    return analyze_skill_gaps(profile)


@app.post("/api/learning-workflow")
def learning_workflow(profile: StudentProfile):
    return coordinate_learning_workflow(profile)


@app.post("/api/code-review")
def code_review_endpoint(request: CodeReviewRequest):
    return review_code(
        code=request.code,
        language=request.language,
    )


@app.post("/api/run-tests")
def run_tests_endpoint(request: TestEvaluationRequest):
    return run_tests(
        timeout_seconds=request.timeout_seconds
    )