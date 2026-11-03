from fastapi import FastAPI

app = FastAPI(
    title="SkillBridge AI",
    description="Multi-agent AI learning and project guidance system",
    version="0.1.0"
)


@app.get("/")
def home():
    return {"message": "Welcome to SkillBridge AI"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}