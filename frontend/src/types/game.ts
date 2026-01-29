/**
 * Game type definitions
 */

export type PieceColor = 'red' | 'black';

export type PieceType = 'K' | 'A' | 'E' | 'H' | 'R' | 'C' | 'P';

export interface Piece {
  type: PieceType;
  color: PieceColor;
}

export interface Position {
  row: number;
  col: number;
}

export interface MoveInfo {
  from: [number, number];
  to: [number, number];
  piece_type: PieceType;
  piece_color: PieceColor;
  captured: { type: PieceType; color: PieceColor } | null;
  is_check: boolean;
  notation: string;
}

export interface ThinkingInfo {
  depth: number;
  nodes_evaluated: number;
  score: number;
}

export type GameResult = 'ongoing' | 'red_win' | 'black_win' | 'draw';

export interface GameState {
  game_id: string;
  board: (Piece | null)[][];
  current_turn: PieceColor;
  game_result: GameResult;
  is_check: boolean;
  move_count: number;
  last_move: { from: [number, number]; to: [number, number] } | null;
  captured_pieces: { type: PieceType; color: PieceColor }[];
  ai_type: string;
  player_color: PieceColor;
}

export interface AIConfig {
  name: string;
  difficulty: number;
  description: string;
  depth?: number;
  time_limit?: number;
}

export type AIType = 'random' | 'greedy' | 'minimax' | 'alphabeta';

// WebSocket message types
export interface WSMessage {
  type: string;
  data: unknown;
}

export interface WSMoveMessage {
  type: 'move';
  data: {
    from_row: number;
    from_col: number;
    to_row: number;
    to_col: number;
  };
}

export interface WSRequestAIMoveMessage {
  type: 'request_ai_move';
  data: Record<string, never>;
}

export interface WSUndoMessage {
  type: 'undo';
  data: { steps: number };
}

export interface WSGetLegalMovesMessage {
  type: 'get_legal_moves';
  data: { row: number; col: number };
}
