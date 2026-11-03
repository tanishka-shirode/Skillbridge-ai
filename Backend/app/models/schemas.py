from pydantic import BaseModel, Field
from typing import Literal


class StudentProfile(BaseModel):
    current_skills: list[str] = Field(min_length=1)
    target_role: str = Field(min_length=2)
    experience_level: Literal["beginner", "intermediate", "advanced"]
    hours_per_week: int = Field(ge=1, le=80)
    learning_preferences: list[str] = []