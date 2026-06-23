"""
models.py — Pydantic data models for the Antigravity Engine.

Every request/response is strictly typed so the "weightless" JSON
contract between backend and the Blue & White UI is never broken.
"""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


# ─────────────────────────── Enums ───────────────────────────

class FitnessLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class Goal(str, Enum):
    MUSCLE_GAIN = "Muscle Gain"
    WEIGHT_LOSS = "Weight Loss"
    ENDURANCE = "Endurance"


# ─────────────────────────── Request ─────────────────────────

class UserProfile(BaseModel):
    """Input payload from the UI."""
    age: int = Field(..., ge=14, le=80, description="User's age in years")
    weight: float = Field(..., gt=30, le=250, description="Body weight in kg")
    fitness_level: FitnessLevel
    goal: Goal


# ─────────────────────────── Response ────────────────────────

class Exercise(BaseModel):
    """Single exercise returned to the UI."""
    exercise_name: str
    sets: int
    reps: str  # can be "12" or "30 sec" for timed exercises
    rest_time: str  # e.g. "60s"
    tutorial_video_url: str
    muscle_group: str
    intensity: str  # Low / Medium / High
    calories_per_set: int
    icon: str  # emoji for the UI cards


class WorkoutDay(BaseModel):
    """A single day in the programme."""
    day: str  # "Day 1 — Push", etc.
    focus: str
    exercises: List[Exercise]
    estimated_duration_min: int
    total_calories: int


class WorkoutPlan(BaseModel):
    """Top-level response — the full programme."""
    plan_name: str
    description: str
    level: FitnessLevel
    goal: Goal
    days_per_week: int
    days: List[WorkoutDay]
    tips: List[str]
    antigravity_mode: bool = False  # 🥚 easter egg flag


class AntigravityEasterEgg(BaseModel):
    """Hidden endpoint response for the easter egg."""
    message: str
    animation: str
    secret_code: str
