from fastapi import FastAPI

from Backend.app.models.schemas import StudentProfile
from Backend.app.agents.skill_mapper import analyze_skill_gaps
from Backend.app.agents.coordinator import coordinate_learning_workflow

app = FastAPI(
    title="SkillBridge AI",
    description="Multi-agent AI learning and project guidance system",
    version="0.4.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SkillBridge AI",
        "version": "0.4.0"
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