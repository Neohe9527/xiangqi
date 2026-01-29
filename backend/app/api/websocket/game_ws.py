"""
WebSocket handler for real-time game communication
"""
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

from app.services.game_service import session_manager


class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = set()
        self.active_connections[game_id].add(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        """Remove a WebSocket connection"""
        if game_id in self.active_connections:
            self.active_connections[game_id].discard(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]

    async def send_to_game(self, game_id: str, message: dict):
        """Send a message to all connections for a game"""
        if game_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[game_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)

            # Clean up disconnected
            for conn in disconnected:
                self.active_connections[game_id].discard(conn)


manager = ConnectionManager()


async def handle_websocket(websocket: WebSocket, game_id: str):
    """Handle WebSocket connection for a game"""
    session = session_manager.get_session(game_id)
    if not session:
        await websocket.close(code=4004, reason="Game not found")
        return

    await manager.connect(websocket, game_id)

    try:
        # Send initial game state
        await websocket.send_json({
            'type': 'game_state',
            'data': session_manager.get_game_state(session)
        })

        while True:
            # Receive message
            data = await websocket.receive_json()
            message_type = data.get('type')

            if message_type == 'move':
                # Handle player move
                move_data = data.get('data', {})
                result = session_manager.make_move(
                    session,
                    move_data.get('from_row'),
                    move_data.get('from_col'),
                    move_data.get('to_row'),
                    move_data.get('to_col')
                )

                if result['success']:
                    await manager.send_to_game(game_id, {
                        'type': 'move_made',
                        'data': result
                    })
                else:
                    await websocket.send_json({
                        'type': 'error',
                        'data': {'message': result['error']}
                    })

            elif message_type == 'request_ai_move':
                # Send thinking notification
                await manager.send_to_game(game_id, {
                    'type': 'ai_thinking',
                    'data': {'status': 'started'}
                })

                # Get AI move (run in thread pool to not block)
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    session_manager.get_ai_move,
                    session
                )

                if result['success']:
                    await manager.send_to_game(game_id, {
                        'type': 'ai_move',
                        'data': result
                    })
                else:
                    await websocket.send_json({
                        'type': 'error',
                        'data': {'message': result['error']}
                    })

            elif message_type == 'undo':
                steps = data.get('data', {}).get('steps', 2)
                result = session_manager.undo_move(session, steps)

                if result['success']:
                    await manager.send_to_game(game_id, {
                        'type': 'undo_done',
                        'data': result
                    })
                else:
                    await websocket.send_json({
                        'type': 'error',
                        'data': {'message': result['error']}
                    })

            elif message_type == 'get_legal_moves':
                move_data = data.get('data', {})
                moves = session_manager.get_legal_moves(
                    session,
                    move_data.get('row'),
                    move_data.get('col')
                )
                await websocket.send_json({
                    'type': 'legal_moves',
                    'data': {'moves': moves}
                })

            elif message_type == 'get_state':
                await websocket.send_json({
                    'type': 'game_state',
                    'data': session_manager.get_game_state(session)
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)
    except Exception as e:
        manager.disconnect(websocket, game_id)
        raise
