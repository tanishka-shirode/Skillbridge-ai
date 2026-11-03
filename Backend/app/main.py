from fastapi import FastAPI
from Backend.app.models.schemas import StudentProfile

app = FastAPI(
    title="SkillBridge AI",
    description="Multi-agent AI learning and project guidance system",
    version="0.2.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SkillBridge AI",
        "version": "0.2.0"
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