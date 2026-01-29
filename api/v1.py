"""
Vercel serverless function for Xiangqi API
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes.games import router as games_router
from backend.app.api.websocket.game_ws import handle_websocket

app = FastAPI(
    title="Xiangqi API",
    description="Chinese Chess (Xiangqi) Game API",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routes
app.include_router(games_router)

@app.get("/")
async def root():
    return {
        "name": "Xiangqi API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
