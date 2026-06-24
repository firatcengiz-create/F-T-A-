import pytest
from backend.models import UserProfile, Goal, FitnessLevel
from backend.generator import _apply_progressive_overload, generate_workout_plan

def test_progressive_overload():
    exercise = {"base_reps": "10", "base_sets": 3}
    # Week 3 Advanced should bump sets and drop reps
    result = _apply_progressive_overload(exercise, week=3, level=FitnessLevel.ADVANCED)
    assert result["base_sets"] == 4
    assert result["base_reps"] == "8"  # 10 - (3 - 1) = 8

@pytest.mark.asyncio
async def test_fallback_generator_structure():
    profile = UserProfile(
        age=25, 
        weight=70.0, 
        height=175.0, 
        goal=Goal.MUSCLE_GAIN, 
        fitness_level=FitnessLevel.BEGINNER
    )
    plan = await generate_workout_plan(profile)
    assert plan.goal == Goal.MUSCLE_GAIN
    assert plan.level == FitnessLevel.BEGINNER
    assert plan.days_per_week == 3
    assert len(plan.days) == 3
    for day in plan.days:
        assert len(day.exercises) == 4
