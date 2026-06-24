"""
generator.py — The Antigravity Engine Core 🚀

This is the heart of the programme generator.  It maps a UserProfile
to a complete, periodised workout plan using rule-based selection and
progressive-overload logic.

Design notes
────────────
• Every public function is ``async`` so FastAPI can serve it without
  blocking the event loop — the "antigravity smoothness" requirement.
• The algorithm is O(n) over the exercise catalogue; no heavy compute
  means the UI stays *weightless*.

# import antigravity   ← we take this literally 😎
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import math
import os
import random
from typing import List

from pydantic import ValidationError

from google import genai

from backend.exercise_db import EXERCISE_DATABASE
from backend.models import (
    Exercise,
    FitnessLevel,
    Goal,
    UserProfile,
    WorkoutDay,
    WorkoutPlan,
)

# ───────────────── Level multipliers ─────────────────────────

_LEVEL_CONFIG = {
    FitnessLevel.BEGINNER: {
        "set_mult": 0.75,
        "rep_mult": 1.0,
        "rest_mult": 1.3,
        "days_per_week": 3,
        "exercises_per_day": 4,
    },
    FitnessLevel.INTERMEDIATE: {
        "set_mult": 1.0,
        "rep_mult": 1.0,
        "rest_mult": 1.0,
        "days_per_week": 4,
        "exercises_per_day": 5,
    },
    FitnessLevel.ADVANCED: {
        "set_mult": 1.25,
        "rep_mult": 1.15,
        "rest_mult": 0.8,
        "days_per_week": 5,
        "exercises_per_day": 6,
    },
}

# ───────────── Goal → day-split templates ────────────────────

_SPLIT_TEMPLATES = {
    Goal.MUSCLE_GAIN: [
        ("İtiş — Göğüs ve Omuz", "Göğüs / Omuz / Arka Kol"),
        ("Çekiş — Sırt ve Pazı", "Sırt / Pazu"),
        ("Bacak — Çömelme Odaklı", "Bacak"),
        ("Üst Vücut Hipertrofi", "Göğüs / Omuz / Sırt"),
        ("Alt Vücut Hipertrofi", "Bacak / Arka Zincir"),
    ],
    Goal.WEIGHT_LOSS: [
        ("HIIT Yanma", "Tüm Vücut / Kardiyo"),
        ("Metabolik Kondisyon", "Tüm Vücut / Kardiyo"),
        ("Kardiyo Merkez Patlaması", "Karın / Kardiyo"),
        ("Tüm Vücut Yakımı", "Tüm Vücut"),
        ("Aktif Dinlenme + LISS", "Kardiyo"),
    ],
    Goal.ENDURANCE: [
        ("Dayanıklılık Devresi A", "Tüm Vücut"),
        ("Kondisyon ve Karın", "Karın / Kardiyo"),
        ("Dayanıklılık Devresi B", "Tüm Vücut"),
        ("Güç-Dayanıklılık", "Bacak / Sırt"),
        ("Kardiyo Aralıkları", "Kardiyo"),
    ],
}

_TIPS = {
    Goal.MUSCLE_GAIN: [
        "Aşamalı yüklenme: ağırlığı her 1-2 haftada bir 2.5 kg artırın.",
        "Günlük vücut ağırlığı başına 1.6–2.2 g protein hedefleyin.",
        "7-9 saat uyuyun — kaslar dinlenme sırasında büyür.",
        "Hipertrofi uyarısını maksimize etmek için dinlenme sürelerine sadık kalın.",
        "Her seansı takip edin. Ölçülen şey yönetilebilir.",
    ],
    Goal.WEIGHT_LOSS: [
        "Sürdürülebilir yağ kaybı için günlük 300-500 kcal açık verin.",
        "Aşırı antrenmandan kaçınmak için HIIT seanslarını 30 dakikanın altında tutun.",
        "Susuz kalmayın — dehidrasyon performansı düşürür.",
        "Antrenmanları günlük 8.000+ adım ile destekleyin.",
        "Öğün atlamayın; bunun yerine besin değeri yüksek yiyecekler seçin.",
    ],
    Goal.ENDURANCE: [
        "Yoğunluğu artırmadan önce güçlü bir aerobik temel oluşturun.",
        "Dönemleme yapın: zor ve kolay haftaları değiştirin.",
        "Antrenmandan 2 saat önce kompleks karbonhidratlarla yakıt alın.",
        "Fitness kazanımlarını takip etmek için dinlenme kalp atış hızınızı izleyin.",
        "Aşırı kullanım yaralanmalarını önlemek için mobilite çalışmaları ekleyin.",
    ],
}


# ─────────────── Helper: adjust reps / rest ──────────────────

def _scale_reps(base_reps: str, mult: float) -> str:
    """Scale numeric reps; leave timed reps (e.g. '30 sec') untouched."""
    try:
        numeric = int(base_reps)
        return str(max(1, math.ceil(numeric * mult)))
    except ValueError:
        return base_reps  # timed or distance-based


def _scale_rest(base_rest: str, mult: float) -> str:
    """Scale rest time string like '90s' or '120s'."""
    numeric = int("".join(c for c in base_rest if c.isdigit()) or "60")
    scaled = max(10, round(numeric * mult / 5) * 5)  # round to 5 s
    return f"{scaled}s"


# ─────────── Progressive-overload modifier (Muscle Gain) ─────

def _apply_progressive_overload(
    exercise: dict, week: int = 1, level: FitnessLevel = FitnessLevel.INTERMEDIATE
) -> dict:
    """
    For Muscle Gain goal: each 'week' the programme suggests slightly
    heavier / more volume.  We bake week-1 defaults but expose the
    logic so the frontend can re-generate for later weeks.
    """
    # Progressive overload: +2.5 % load increase per week (applied externally)
    ex = exercise.copy()
    try:
        reps = int(ex["base_reps"])
        # drop reps slightly as weight increases
        ex["base_reps"] = str(max(4, reps - (week - 1)))
    except ValueError:
        pass
    # bump sets for advanced lifters in later weeks
    if level == FitnessLevel.ADVANCED and week >= 3:
        ex["base_sets"] = min(ex["base_sets"] + 1, 6)
    return ex


# ──────────────── Core selection algorithm ───────────────────

async def _select_exercises(
    goal: Goal,
    level: FitnessLevel,
    count: int,
    day_focus: str,
) -> List[Exercise]:
    """
    Pick *count* exercises from the DB that match the goal.

    Priority rules
    ──────────────
    • Weight Loss  → HIIT / Cardio first
    • Muscle Gain  → Compound lifts first, then isolation
    • Endurance    → Mixed conditioning

    The function is async so it can be awaited without blocking.
    """
    cfg = _LEVEL_CONFIG[level]

    # 1. Score every exercise
    scored: list[tuple[float, dict]] = []
    for ex in EXERCISE_DATABASE:
        score = 0.0
        if goal.value in ex["goals"]:
            score += 10.0
        # bonus for intensity alignment
        if goal == Goal.WEIGHT_LOSS and ex["intensity"] == "High":
            score += 3.0
        if goal == Goal.MUSCLE_GAIN and ex["intensity"] == "High":
            score += 4.0
        if goal == Goal.ENDURANCE and ex["intensity"] == "Medium":
            score += 2.0
        # small random jitter so plans feel fresh
        score += random.uniform(0, 2)
        scored.append((score, ex))

    # 2. Sort descending and pick top-n
    scored.sort(key=lambda t: t[0], reverse=True)
    picked = [ex for _, ex in scored[:count]]

    # 3. Build Exercise models with level scaling
    result: List[Exercise] = []
    for ex in picked:
        if goal == Goal.MUSCLE_GAIN:
            ex = _apply_progressive_overload(ex, week=1, level=level)

        sets = max(1, round(ex["base_sets"] * cfg["set_mult"]))
        reps = _scale_reps(ex["base_reps"], cfg["rep_mult"])
        rest = _scale_rest(ex["rest"], cfg["rest_mult"])

        result.append(
            Exercise(
                exercise_name=ex["name"],
                sets=sets,
                reps=reps,
                rest_time=rest,
                tutorial_video_url=ex["video"],
                muscle_group=ex["muscle_group"],
                intensity=ex["intensity"],
                calories_per_set=ex["cal_per_set"],
                icon=ex["icon"],
            )
        )

    # simulate a tiny async delay (e.g. future DB call)
    await asyncio.sleep(0)
    return result


# ───────────────── Public API ────────────────────────────────

async def _generate_workout_plan_ai(profile: UserProfile, api_key: str) -> WorkoutPlan:
    """Uses Gemini to generate the structured workout plan asynchronously."""
    client = genai.Client(api_key=api_key)
    prompt = (
        f"Act as a professional fitness coach. "
        f"Generate a {profile.fitness_level.value} level {profile.goal.value} workout plan "
        f"for a {profile.age} year old weighing {profile.weight} kg. "
        f"Be creative but realistic with the exercises and follow the requested schema. "
        f"IMPORTANT: Generate the entire response (including plan names, descriptions, day focus, and tips) in Turkish, "
        f"EXCEPT for the 'exercise_name' fields, which MUST remain in English."
    )
    response = await client.aio.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=WorkoutPlan,
        ),
    )
    return WorkoutPlan.model_validate_json(response.text)


async def generate_workout_plan(profile: UserProfile) -> WorkoutPlan:
    """
    Top-level generator — turns a UserProfile into a full WorkoutPlan.

    This is the single function the FastAPI route calls.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            return await _generate_workout_plan_ai(profile, api_key)
        except ValidationError as e:
            print(f"AI Generation validation failed: {e}. Falling back to rule-based.")
        except Exception as e:
            print(f"AI Generation failed: {e}. Falling back to rule-based.")

    cfg = _LEVEL_CONFIG[profile.fitness_level]
    days_per_week = cfg["days_per_week"]
    ex_per_day = cfg["exercises_per_day"]

    split = _SPLIT_TEMPLATES[profile.goal][:days_per_week]

    # Build each day concurrently for maximum responsiveness
    day_tasks = [
        _select_exercises(profile.goal, profile.fitness_level, ex_per_day, focus)
        for label, focus in split
    ]
    day_exercises = await asyncio.gather(*day_tasks)

    days: List[WorkoutDay] = []
    for idx, ((label, focus), exercises) in enumerate(
        zip(split, day_exercises), start=1
    ):
        total_cal = sum(e.calories_per_set * e.sets for e in exercises)
        est_min = sum(
            e.sets * 2  # ~2 min per set including rest
            for e in exercises
        )
        days.append(
            WorkoutDay(
                day=f"{idx}. Gün — {label}",
                focus=focus,
                exercises=exercises,
                estimated_duration_min=est_min,
                total_calories=total_cal,
            )
        )

    goal_label = {
        Goal.MUSCLE_GAIN: "Kas Geliştirme",
        Goal.WEIGHT_LOSS: "Kilo Verme",
        Goal.ENDURANCE: "Dayanıklılık",
    }[profile.goal]

    level_label = {
        FitnessLevel.BEGINNER: "Başlangıç",
        FitnessLevel.INTERMEDIATE: "Orta",
        FitnessLevel.ADVANCED: "İleri",
    }[profile.fitness_level]

    plan = WorkoutPlan(
        plan_name=f"Antigravity {goal_label} Programı",
        description=(
            f"{profile.age} yaşında, {profile.weight} kg {level_label.lower()} seviye "
            f"sporcu için hazırlanmış {days_per_week} günlük {goal_label.lower()} planı."
        ),
        level=profile.fitness_level,
        goal=profile.goal,
        days_per_week=days_per_week,
        days=days,
        tips=_TIPS[profile.goal],
        antigravity_mode=False,
    )
    return plan
