from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class Category(str, Enum):
    WORK = "work"
    STUDY = "study"
    PERSONAL = "personal"
    HEALTH = "health"
    HOUSEHOLD = "household"
    SOCIAL = "social"
    ADMIN = "admin"
    OTHER = "other"


class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExtractedTask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        description="Short, actionable task title."
    )
    description: Optional[str] = None

    category: Optional[Category] = None

    deadline_text: Optional[str] = Field(
        default=None,
        description="Original deadline expression from the user."
    )
    start_time_text: Optional[str] = None

    estimated_duration_minutes: Optional[int] = Field(
        default=None,
        ge=1,
    )

    urgency: Optional[Urgency] = None

    energy_required: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="Only extract if explicitly stated."
    )

    location: Optional[str] = None

    dependencies: list[str] = Field(default_factory=list)

    is_recurring: bool = False
    recurrence_text: Optional[str] = None

    completion_criteria: Optional[str] = None


class TaskExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tasks: list[ExtractedTask]

    clarification_needed: bool = False
    clarification_questions: list[str] = Field(
        default_factory=list
    )
