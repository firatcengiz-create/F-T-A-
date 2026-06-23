"""
main.py — FastAPI application for the Antigravity Fitness Engine 🚀

Endpoints
─────────
POST /api/generate    → Generate a workout plan from a UserProfile.
GET  /api/antigravity  → 🥚 Easter-egg endpoint.
GET  /                → Serve the frontend.

Run:
    uvicorn backend.main:app --reload --port 8000
"""

from __future__ import annotations

# import antigravity  # noqa  ← 🥚 Python's real easter egg!
#                      # We honour it with our own floating animation instead.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.generator import generate_workout_plan
from backend.models import AntigravityEasterEgg, UserProfile, WorkoutPlan

# ─────────────────── App setup ───────────────────────────────

app = FastAPI(
    title="Antigravity Fitness Engine",
    version="1.0.0",
    description="Weightless workout generation — powered by async Python.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────── Static files (frontend) ─────────────────────

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ─────────────────── Routes ──────────────────────────────────

@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the single-page frontend."""
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/api/generate", response_model=WorkoutPlan)
async def generate(profile: UserProfile) -> WorkoutPlan:
    """
    Generate a personalised workout plan.

    The entire pipeline is async — the event loop is never blocked,
    keeping the UI buttery smooth (the *antigravity* promise).
    """
    plan = await generate_workout_plan(profile)
    return plan


@app.get("/api/antigravity", response_model=AntigravityEasterEgg)
async def easter_egg():
    """
    🥚  ``import antigravity``

    Hit this endpoint to unlock the floating animation in the UI.
    """
    return AntigravityEasterEgg(
        message="You found the easter egg! 🎉  import antigravity activated.",
        animation="float",
        secret_code="WEIGHTLESS-42",
    )

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 adresi yerel ağdaki (telefon vb.) diğer cihazların bağlanmasına izin verir.
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
