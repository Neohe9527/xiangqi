"""
FastAPI main application entry point
"""
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.games import router as games_router
from app.api.websocket.game_ws import handle_websocket

app = FastAPI(
    title="Xiangqi API",
    description="Chinese Chess (Xiangqi) Game API",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routes
app.include_router(games_router)


# WebSocket endpoint
@app.websocket("/ws/games/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    await handle_websocket(websocket, game_id)


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
