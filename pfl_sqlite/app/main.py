from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import player_router, club_router  # Import your routers
from app.schemas import __init__
from app.routers.financial_log_router import router as financial_log_router

# Load .env variables
load_dotenv()

# 🧠 Init FastAPI app
app = FastAPI(
    title="PFL API - Pirate Football League",
    description="Backend API for managing players, matches, clubs, and more in the PFL universe.",
    version="1.0.0",
)

# 🌐 Enable CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Import routers AFTER app is created
from app.routers import (
    admin_log_router,
    player_router,
    season_router,
    transfer_router,
    match_router,
    user_router,
    club_router,
    training_router,
    auth_router,
    tick_router,
    matchday_router,
    league_standing_router
  # Discord login etc
)

# 📡 Include API routers
app.include_router(admin_log_router.router, prefix="/admin_logs", tags=["Admin Logs"])
app.include_router(player_router.router, tags=["Players"])
app.include_router(season_router.router, prefix="/seasons", tags=["Seasons"])
app.include_router(transfer_router.router, prefix="/transfers", tags=["Transfers"])
app.include_router(match_router.router, prefix="/matches", tags=["Matches"])
app.include_router(training_router.router, prefix="/training", tags=["Training Sessions"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(club_router.router, prefix="/clubs", tags=["Clubs"])
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(tick_router.router)
app.include_router(matchday_router.router)
app.include_router(league_standing_router.router)
app.include_router(financial_log_router)
  # Discord login / callback

# 🧪 Optional: healthcheck
@app.get("/")
def root():
    return {"status": "PFL backend is alive 🧠⚽", "version": "1.0.0"}
