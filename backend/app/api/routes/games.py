"""
Game REST API routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.services.game_service import session_manager
from app import config

router = APIRouter(prefix="/api/v1/games", tags=["games"])


class CreateGameRequest(BaseModel):
    ai_type: str = 'alphabeta'
    player_color: str = 'red'


class MoveRequest(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int


class UndoRequest(BaseModel):
    steps: int = 2


class LegalMovesRequest(BaseModel):
    row: int
    col: int


@router.post("")
async def create_game(request: CreateGameRequest):
    """Create a new game session"""
    if request.ai_type not in config.AI_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Invalid AI type: {request.ai_type}")

    if request.player_color not in ['red', 'black']:
        raise HTTPException(status_code=400, detail="Player color must be 'red' or 'black'")

    session = session_manager.create_session(
        ai_type=request.ai_type,
        player_color=request.player_color
    )

    return {
        'game_id': session.game_id,
        'game_state': session_manager.get_game_state(session),
        'ai_config': config.AI_CONFIGS.get(request.ai_type)
    }


@router.get("/{game_id}")
async def get_game(game_id: str):
    """Get game state by ID"""
    session = session_manager.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")

    return session_manager.get_game_state(session)


@router.delete("/{game_id}")
async def delete_game(game_id: str):
    """Delete a game session"""
    if not session_manager.delete_session(game_id):
        raise HTTPException(status_code=404, detail="Game not found")

    return {'success': True}


@router.post("/{game_id}/moves")
async def make_move(game_id: str, request: MoveRequest):
    """Make a move in the game"""
    session = session_manager.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")

    result = session_manager.make_move(
        session,
        request.from_row, request.from_col,
        request.to_row, request.to_col
    )

    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])

    return result


@router.post("/{game_id}/ai-move")
async def get_ai_move(game_id: str):
    """Request AI to make a move"""
    session = session_manager.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")

    result = session_manager.get_ai_move(session)

    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])

    return result


@router.post("/{game_id}/undo")
async def undo_move(game_id: str, request: UndoRequest):
    """Undo moves"""
    session = session_manager.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")

    result = session_manager.undo_move(session, request.steps)

    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])

    return result


@router.post("/{game_id}/legal-moves")
async def get_legal_moves(game_id: str, request: LegalMovesRequest):
    """Get legal moves for a piece"""
    session = session_manager.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")

    moves = session_manager.get_legal_moves(session, request.row, request.col)

    return {'legal_moves': moves}


@router.get("/config/ai-types")
async def get_ai_types():
    """Get available AI types and their configurations"""
    return config.AI_CONFIGS
