"""
Game session service - manages game state for each session
"""
import uuid
import time
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass, field

from app.core.board import Board
from app.core.move import Move
from app.core.rules import is_in_check, is_checkmate, get_game_result, is_legal_move
from app.ai.random_ai import RandomAI
from app.ai.greedy_ai import GreedyAI
from app.ai.minimax_ai import MinimaxAI
from app.ai.alphabeta_ai import AlphaBetaAI
from app.ai.master_ai import MasterAI
from app import config


@dataclass
class MoveRecord:
    """Record of a single move"""
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    piece_type: str
    piece_color: str
    captured_type: Optional[str] = None
    captured_color: Optional[str] = None
    is_check: bool = False
    notation: str = ""


@dataclass
class GameSession:
    """Represents a single game session"""
    game_id: str
    board: Board
    current_turn: str = 'red'
    game_result: str = 'ongoing'
    move_history: List[MoveRecord] = field(default_factory=list)
    captured_pieces: List[dict] = field(default_factory=list)
    ai_type: str = 'alphabeta'
    player_color: str = 'red'
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)

    # Internal state for undo
    _move_stack: List[Tuple[Move, any]] = field(default_factory=list)


class GameSessionManager:
    """Manages all game sessions"""

    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}
        self._ai_cache: Dict[str, any] = {}

    def create_session(
        self,
        ai_type: str = 'alphabeta',
        player_color: str = 'red'
    ) -> GameSession:
        """Create a new game session"""
        game_id = str(uuid.uuid4())
        board = Board()

        session = GameSession(
            game_id=game_id,
            board=board,
            ai_type=ai_type,
            player_color=player_color
        )

        self.sessions[game_id] = session
        self._cleanup_old_sessions()

        return session

    def get_session(self, game_id: str) -> Optional[GameSession]:
        """Get a game session by ID"""
        session = self.sessions.get(game_id)
        if session:
            session.last_activity = time.time()
        return session

    def delete_session(self, game_id: str) -> bool:
        """Delete a game session"""
        if game_id in self.sessions:
            del self.sessions[game_id]
            return True
        return False

    def _cleanup_old_sessions(self):
        """Remove sessions that have been inactive for too long"""
        current_time = time.time()
        expired_ids = [
            gid for gid, session in self.sessions.items()
            if current_time - session.last_activity > config.SESSION_TIMEOUT
        ]
        for gid in expired_ids:
            del self.sessions[gid]

        # Also limit total sessions
        if len(self.sessions) > config.MAX_SESSIONS:
            # Remove oldest sessions
            sorted_sessions = sorted(
                self.sessions.items(),
                key=lambda x: x[1].last_activity
            )
            for gid, _ in sorted_sessions[:len(self.sessions) - config.MAX_SESSIONS]:
                del self.sessions[gid]

    def get_ai(self, ai_type: str, color: str):
        """Get or create an AI instance"""
        cache_key = f"{ai_type}_{color}"

        if cache_key not in self._ai_cache:
            if ai_type == 'random':
                self._ai_cache[cache_key] = RandomAI(color)
            elif ai_type == 'greedy':
                self._ai_cache[cache_key] = GreedyAI(color)
            elif ai_type == 'minimax':
                ai_config = config.AI_CONFIGS.get('minimax', {})
                self._ai_cache[cache_key] = MinimaxAI(color, depth=ai_config.get('depth', 3))
            elif ai_type == 'master':
                ai_config = config.AI_CONFIGS.get('master', {})
                self._ai_cache[cache_key] = MasterAI(
                    color,
                    depth=ai_config.get('depth', 10),
                    time_limit=ai_config.get('time_limit', 60),
                    quiescence_depth=ai_config.get('quiescence_depth', 8)
                )
            else:  # alphabeta
                ai_config = config.AI_CONFIGS.get('alphabeta', {})
                self._ai_cache[cache_key] = AlphaBetaAI(
                    color,
                    depth=ai_config.get('depth', 8),
                    time_limit=ai_config.get('time_limit', 30)
                )

        return self._ai_cache[cache_key]

    def make_move(
        self,
        session: GameSession,
        from_row: int,
        from_col: int,
        to_row: int,
        to_col: int
    ) -> dict:
        """
        Make a move in the game

        Returns:
            dict with keys: success, error, move_info, game_state
        """
        if session.game_result != 'ongoing':
            return {'success': False, 'error': 'Game has ended'}

        board = session.board
        piece = board.get_piece(from_row, from_col)

        if not piece:
            return {'success': False, 'error': 'No piece at source position'}

        if piece.color != session.current_turn:
            return {'success': False, 'error': 'Not your turn'}

        # Find the move in legal moves
        legal_moves = board.get_legal_moves(session.current_turn)
        target_move = None

        for move in legal_moves:
            if (move.from_row == from_row and move.from_col == from_col and
                move.to_row == to_row and move.to_col == to_col):
                target_move = move
                break

        if not target_move:
            return {'success': False, 'error': 'Illegal move'}

        # Execute the move
        captured = board.make_move(target_move)

        # Record for undo
        session._move_stack.append((target_move, captured))

        # Create move record
        move_record = MoveRecord(
            from_pos=(from_row, from_col),
            to_pos=(to_row, to_col),
            piece_type=piece.type,
            piece_color=piece.color,
            captured_type=captured.type if captured else None,
            captured_color=captured.color if captured else None,
            notation=target_move.to_chinese()
        )

        # Switch turn
        session.current_turn = 'black' if session.current_turn == 'red' else 'red'

        # Check for check
        move_record.is_check = is_in_check(board, session.current_turn)

        session.move_history.append(move_record)

        if captured:
            session.captured_pieces.append({
                'type': captured.type,
                'color': captured.color
            })

        # Check game result
        session.game_result = get_game_result(board, session.current_turn)
        session.last_activity = time.time()

        return {
            'success': True,
            'move_info': {
                'from': [from_row, from_col],
                'to': [to_row, to_col],
                'piece_type': piece.type,
                'piece_color': piece.color,
                'captured': {'type': captured.type, 'color': captured.color} if captured else None,
                'is_check': move_record.is_check,
                'notation': move_record.notation
            },
            'game_state': self.get_game_state(session)
        }

    def get_ai_move(self, session: GameSession) -> dict:
        """
        Get AI's move for the current position

        Returns:
            dict with keys: success, error, move_info, thinking_info, game_state
        """
        if session.game_result != 'ongoing':
            return {'success': False, 'error': 'Game has ended'}

        # Determine AI color
        ai_color = 'black' if session.player_color == 'red' else 'red'

        if session.current_turn != ai_color:
            return {'success': False, 'error': 'Not AI turn'}

        ai = self.get_ai(session.ai_type, ai_color)
        move = ai.get_move(session.board)

        if not move:
            return {'success': False, 'error': 'AI could not find a move'}

        # Get thinking info before making the move
        thinking_info = ai.get_thinking_info()

        # Make the move
        result = self.make_move(
            session,
            move.from_row, move.from_col,
            move.to_row, move.to_col
        )

        if result['success']:
            result['thinking_info'] = {
                'depth': thinking_info.get('depth', 0),
                'nodes_evaluated': thinking_info.get('nodes_evaluated', 0),
                'score': thinking_info.get('score', 0)
            }

        return result

    def undo_move(self, session: GameSession, steps: int = 2) -> dict:
        """
        Undo moves (default 2 for human-AI game)

        Returns:
            dict with keys: success, error, game_state
        """
        if len(session._move_stack) < steps:
            return {'success': False, 'error': 'Not enough moves to undo'}

        for _ in range(steps):
            move, captured = session._move_stack.pop()
            session.board.undo_move(move, captured)
            session.current_turn = 'black' if session.current_turn == 'red' else 'red'

            if session.move_history:
                session.move_history.pop()

            if captured and session.captured_pieces:
                session.captured_pieces.pop()

        session.game_result = 'ongoing'
        session.last_activity = time.time()

        return {
            'success': True,
            'game_state': self.get_game_state(session)
        }

    def get_legal_moves(self, session: GameSession, row: int, col: int) -> List[List[int]]:
        """Get legal moves for a piece at the given position"""
        piece = session.board.get_piece(row, col)
        if not piece or piece.color != session.current_turn:
            return []

        legal_moves = session.board.get_legal_moves(session.current_turn)
        return [
            [move.to_row, move.to_col]
            for move in legal_moves
            if move.from_row == row and move.from_col == col
        ]

    def get_game_state(self, session: GameSession) -> dict:
        """Get the current game state as a dictionary"""
        board_state = []
        for row in range(10):
            row_data = []
            for col in range(9):
                piece = session.board.get_piece(row, col)
                if piece:
                    row_data.append({
                        'type': piece.type,
                        'color': piece.color
                    })
                else:
                    row_data.append(None)
            board_state.append(row_data)

        return {
            'game_id': session.game_id,
            'board': board_state,
            'current_turn': session.current_turn,
            'game_result': session.game_result,
            'is_check': is_in_check(session.board, session.current_turn),
            'move_count': len(session.move_history),
            'last_move': {
                'from': list(session.move_history[-1].from_pos),
                'to': list(session.move_history[-1].to_pos)
            } if session.move_history else None,
            'captured_pieces': session.captured_pieces,
            'ai_type': session.ai_type,
            'player_color': session.player_color
        }


# Global session manager instance
session_manager = GameSessionManager()
