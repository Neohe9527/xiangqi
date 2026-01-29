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
              // 还没跳过棋子
              if (!target) {
                // 空位，可以移动
                moves.push([r, c]);
              } else {
                // 遇到棋子，标记为已跳过
                jumped = true;
              }
            } else {
              // 已经跳过一个棋子
              if (target) {
                // 遇到第二个棋子
                if (target.color !== color) {
                  // 对方棋子，可以吃
                  moves.push([r, c]);
                }
                // 无论如何都要停止（己方或对方棋子都停止）
                break;
              }
              // 如果是空位，继续寻找下一个棋子
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

// Store game state for mock API
let currentGameState: GameState | null = null;

// Piece values for AI evaluation
const PIECE_VALUES: Record<string, number> = {
  'K': 10000, // 将/帅
  'A': 200,   // 士
  'E': 200,   // 象
  'H': 400,   // 马
  'R': 500,   // 车
  'C': 450,   // 炮
  'P': 100,   // 兵/卒
};

// Evaluate a move: returns score (higher is better for AI)
function evaluateMove(
  board: (Piece | null)[][],
  fromRow: number,
  fromCol: number,
  toRow: number,
  toCol: number,
  aiColor: 'red' | 'black'
): number {
  let score = 0;

  // Check if this move captures a piece
  const targetPiece = board[toRow]?.[toCol];
  if (targetPiece && targetPiece.color !== aiColor) {
    // Prioritize capturing valuable pieces
    score += (PIECE_VALUES[targetPiece.type] || 0) * 10;
  }

  // Prefer moving pieces that are under attack (defensive)
  const piece = board[fromRow]?.[fromCol];
  if (piece) {
    // Bonus for moving pieces forward (aggressive)
    if (aiColor === 'red' && toRow < fromRow) {
      score += 5;
    } else if (aiColor === 'black' && toRow > fromRow) {
      score += 5;
    }

    // Bonus for protecting the king
    if (piece.type === 'K') {
      score += 1000; // King moves are important
    }
  }

  // Add some randomness to avoid predictable play
  score += Math.random() * 10;

  return score;
}

// Get best move for AI
function getBestAIMove(
  board: (Piece | null)[][],
  aiColor: 'red' | 'black'
): { from: [number, number]; to: [number, number] } | null {
  const possibleMoves: Array<{
    from: [number, number];
    to: [number, number];
    score: number;
  }> = [];

  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      const piece = board[r]?.[c];
      if (piece && piece.color === aiColor) {
        const moves = getLegalMovesForPiece(board, r, c);
        for (const [toR, toC] of moves) {
          const score = evaluateMove(board, r, c, toR, toC, aiColor);
          possibleMoves.push({
            from: [r, c],
            to: [toR, toC],
            score,
          });
        }
      }
    }
  }

  if (possibleMoves.length === 0) return null;

  // Sort by score and pick the best one
  possibleMoves.sort((a, b) => b.score - a.score);
  return {
    from: possibleMoves[0].from,
    to: possibleMoves[0].to,
  };
}

export const mockAPI = {
  async createGame(
    _aiType: AIType = 'alphabeta',
    _playerColor: 'red' | 'black' = 'red'
  ): Promise<{ game_id: string; game_state: GameState; ai_config: AIConfig }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        currentGameState = createMockGameState();
        resolve({
          game_id: currentGameState.game_id,
          game_state: currentGameState,
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
    return currentGameState || createMockGameState();
  },

  async makeMove(
    _gameId: string,
    fromRow: number,
    fromCol: number,
    toRow: number,
    toCol: number
  ): Promise<{ success: boolean; move_info: unknown; game_state: GameState }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (!currentGameState) {
          currentGameState = createMockGameState();
        }

        // Make the move
        const piece = currentGameState.board[fromRow]?.[toCol];
        currentGameState.board[toRow][toCol] = currentGameState.board[fromRow][fromCol];
        currentGameState.board[fromRow][fromCol] = null;

        // Update game state
        currentGameState.current_turn = currentGameState.current_turn === 'red' ? 'black' : 'red';
        currentGameState.last_move = { from: [fromRow, fromCol], to: [toRow, toCol] };
        currentGameState.move_count += 1;

        // If a piece was captured, add it to captured pieces
        if (piece) {
          currentGameState.captured_pieces.push(piece);
        }

        resolve({
          success: true,
          move_info: {},
          game_state: currentGameState,
        });
      }, 300);
    });
  },

  async requestAIMove(
    _gameId: string
  ): Promise<{ success: boolean; move_info: unknown; thinking_info: unknown; game_state: GameState }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (!currentGameState) {
          currentGameState = createMockGameState();
        }

        // Get the best move for AI using evaluation function
        const move = getBestAIMove(currentGameState.board, currentGameState.current_turn);

        if (move) {
          const piece = currentGameState.board[move.from[0]][move.from[1]];
          const captured = currentGameState.board[move.to[0]][move.to[1]];

          currentGameState.board[move.to[0]][move.to[1]] = piece;
          currentGameState.board[move.from[0]][move.from[1]] = null;
          currentGameState.current_turn = currentGameState.current_turn === 'red' ? 'black' : 'red';
          currentGameState.last_move = { from: move.from, to: move.to };
          currentGameState.move_count += 1;

          if (captured) {
            currentGameState.captured_pieces.push(captured);
          }
        }

        resolve({
          success: true,
          move_info: {},
          thinking_info: { depth: 5, nodes_evaluated: 1000, score: 0 },
          game_state: currentGameState,
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
        // Reset to initial state for mock
        currentGameState = createMockGameState();
        resolve({
          success: true,
          game_state: currentGameState,
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
        if (!currentGameState) {
          currentGameState = createMockGameState();
        }
        const moves = getLegalMovesForPiece(currentGameState.board, row, col);
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
