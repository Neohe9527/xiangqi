/**
 * Mock API for demonstration when backend is not available
 */

import type { GameState, AIType, AIConfig, Piece } from '../types/game';

// Mock game state
const createMockGameState = (): GameState => ({
  game_id: 'mock-game-' + Date.now(),
  board: [
    [
      { type: 'R', color: 'black' },
      { type: 'H', color: 'black' },
      { type: 'E', color: 'black' },
      { type: 'A', color: 'black' },
      { type: 'K', color: 'black' },
      { type: 'A', color: 'black' },
      { type: 'E', color: 'black' },
      { type: 'H', color: 'black' },
      { type: 'R', color: 'black' },
    ],
    [null, null, null, null, null, null, null, null, null],
    [null, { type: 'C', color: 'black' }, null, null, null, null, null, { type: 'C', color: 'black' }, null],
    [
      { type: 'P', color: 'black' },
      null,
      { type: 'P', color: 'black' },
      null,
      { type: 'P', color: 'black' },
      null,
      { type: 'P', color: 'black' },
      null,
      { type: 'P', color: 'black' },
    ],
    [null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null],
    [
      { type: 'P', color: 'red' },
      null,
      { type: 'P', color: 'red' },
      null,
      { type: 'P', color: 'red' },
      null,
      { type: 'P', color: 'red' },
      null,
      { type: 'P', color: 'red' },
    ],
    [null, { type: 'C', color: 'red' }, null, null, null, null, null, { type: 'C', color: 'red' }, null],
    [null, null, null, null, null, null, null, null, null],
    [
      { type: 'R', color: 'red' },
      { type: 'H', color: 'red' },
      { type: 'E', color: 'red' },
      { type: 'A', color: 'red' },
      { type: 'K', color: 'red' },
      { type: 'A', color: 'red' },
      { type: 'E', color: 'red' },
      { type: 'H', color: 'red' },
      { type: 'R', color: 'red' },
    ],
  ],
  current_turn: 'red',
  game_result: 'ongoing',
  last_move: null,
  is_check: false,
  move_count: 0,
  captured_pieces: [],
  ai_type: 'alphabeta',
  player_color: 'red',
});

// Helper function to get legal moves for a piece
function getLegalMovesForPiece(
  board: (Piece | null)[][],
  row: number,
  col: number
): [number, number][] {
  const piece = board[row]?.[col];
  if (!piece) return [];

  const moves: [number, number][] = [];
  const { type, color } = piece;

  const addMove = (r: number, c: number) => {
    if (r >= 0 && r < 10 && c >= 0 && c < 9) {
      const target = board[r]?.[c];
      if (!target || target.color !== color) {
        moves.push([r, c]);
      }
    }
  };

  const addMovesInDirection = (dr: number, dc: number, maxDistance: number = 10) => {
    for (let i = 1; i < maxDistance; i++) {
      const r = row + dr * i;
      const c = col + dc * i;
      if (r < 0 || r >= 10 || c < 0 || c >= 9) break;

      const target = board[r]?.[c];
      if (!target) {
        moves.push([r, c]);
      } else {
        if (target.color !== color) {
          moves.push([r, c]);
        }
        break;
      }
    }
  };

  switch (type) {
    case 'K': // 将/帅 - 在九宫格内移动一步
      {
        const [rowMin, rowMax] = color === 'red' ? [7, 9] : [0, 2];
        const [colMin, colMax] = [3, 5];
        const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        for (const [dr, dc] of directions) {
          const r = row + dr;
          const c = col + dc;
          if (r >= rowMin && r <= rowMax && c >= colMin && c <= colMax) {
            addMove(r, c);
          }
        }
      }
      break;

    case 'A': // 士 - 在九宫格内斜着走
      {
        const [rowMin, rowMax] = color === 'red' ? [7, 9] : [0, 2];
        const [colMin, colMax] = [3, 5];
        const directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
        for (const [dr, dc] of directions) {
          const r = row + dr;
          const c = col + dc;
          if (r >= rowMin && r <= rowMax && c >= colMin && c <= colMax) {
            addMove(r, c);
          }
        }
      }
      break;

    case 'E': // 象/相 - 走田字，不能过河
      {
        const rowLimit = color === 'red' ? 5 : 4;
        const directions = [[2, 2], [2, -2], [-2, 2], [-2, -2]];
        for (const [dr, dc] of directions) {
          const r = row + dr;
          const c = col + dc;
          if (r >= 0 && r < 10 && c >= 0 && c < 9) {
            // 检查是否过河
            if ((color === 'red' && r >= rowLimit) || (color === 'black' && r <= rowLimit)) {
              // 检查象眼是否被堵
              const eyeR = row + dr / 2;
              const eyeC = col + dc / 2;
              if (!board[eyeR]?.[eyeC]) {
                addMove(r, c);
              }
            }
          }
        }
      }
      break;

    case 'H': // 马 - 走日字
      {
        const directions = [
          [1, 2], [1, -2], [-1, 2], [-1, -2],
          [2, 1], [2, -1], [-2, 1], [-2, -1],
        ];
        for (const [dr, dc] of directions) {
          const r = row + dr;
          const c = col + dc;
          if (r >= 0 && r < 10 && c >= 0 && c < 9) {
            // 检查马腿是否被堵
            const legR = row + (dr > 0 ? 1 : dr < 0 ? -1 : 0);
            const legC = col + (dc > 0 ? 1 : dc < 0 ? -1 : 0);
            if (!board[legR]?.[legC]) {
              addMove(r, c);
            }
          }
        }
      }
      break;

    case 'R': // 车 - 直线移动任意距离
      {
        const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        for (const [dr, dc] of directions) {
          addMovesInDirection(dr, dc);
        }
      }
      break;

    case 'C': // 炮 - 移动时不能越子，吃子时必须隔一个子
      {
        const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        for (const [dr, dc] of directions) {
          let jumped = false;
          for (let i = 1; i < 10; i++) {
            const r = row + dr * i;
            const c = col + dc * i;
            if (r < 0 || r >= 10 || c < 0 || c >= 9) break;

            const target = board[r]?.[c];
            if (!jumped) {
              if (!target) {
                moves.push([r, c]);
              } else {
                jumped = true;
              }
            } else {
              if (target && target.color !== color) {
                moves.push([r, c]);
              }
              break;
            }
          }
        }
      }
      break;

    case 'P': // 兵/卒 - 过河前只能前进，过河后可以左右移动
      {
        const [forward, riverLine] = color === 'red' ? [-1, 4] : [1, 5];
        const crossed = color === 'red' ? row <= riverLine : row >= riverLine;

        // 向前走
        const r = row + forward;
        if (r >= 0 && r < 10) {
          addMove(r, col);
        }

        // 如果已过河，可以左右走
        if (crossed) {
          addMove(row, col - 1);
          addMove(row, col + 1);
        }
      }
      break;
  }

  return moves;
}

export const mockAPI = {
  async createGame(
    _aiType: AIType = 'alphabeta',
    _playerColor: 'red' | 'black' = 'red'
  ): Promise<{ game_id: string; game_state: GameState; ai_config: AIConfig }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const gameState = createMockGameState();
        resolve({
          game_id: gameState.game_id,
          game_state: gameState,
          ai_config: {
            name: 'Mock AI',
            description: 'Mock AI for demonstration',
            difficulty: 1,
          },
        });
      }, 500);
    });
  },

  async getGame(): Promise<GameState> {
    return createMockGameState();
  },

  async makeMove(
    _gameId: string,
    _fromRow: number,
    _fromCol: number,
    _toRow: number,
    _toCol: number
  ): Promise<{ success: boolean; move_info: unknown; game_state: GameState }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const gameState = createMockGameState();
        gameState.current_turn = gameState.current_turn === 'red' ? 'black' : 'red';
        resolve({
          success: true,
          move_info: {},
          game_state: gameState,
        });
      }, 300);
    });
  },

  async requestAIMove(
    _gameId: string
  ): Promise<{ success: boolean; move_info: unknown; thinking_info: unknown; game_state: GameState }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const gameState = createMockGameState();
        gameState.current_turn = 'red';
        resolve({
          success: true,
          move_info: {},
          thinking_info: { depth: 5, nodes_evaluated: 1000, score: 0 },
          game_state: gameState,
        });
      }, 1000);
    });
  },

  async undoMove(
    _gameId: string,
    _steps: number = 2
  ): Promise<{ success: boolean; game_state: GameState }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          game_state: createMockGameState(),
        });
      }, 300);
    });
  },

  async getLegalMoves(
    _gameId: string,
    row: number,
    col: number
  ): Promise<{ legal_moves: [number, number][] }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const gameState = createMockGameState();
        const moves = getLegalMovesForPiece(gameState.board, row, col);
        resolve({
          legal_moves: moves,
        });
      }, 100);
    });
  },

  async getAITypes(): Promise<Record<string, AIConfig>> {
    return {
      random: {
        name: 'Random',
        description: 'Random move selection',
        difficulty: 0,
      },
      alphabeta: {
        name: 'Alpha-Beta',
        description: 'Alpha-Beta pruning algorithm',
        difficulty: 1,
      },
    };
  },

  getWebSocketUrl(): string {
    return '';
  },
};
