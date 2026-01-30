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

// Position values for pieces (simplified from professional engines)
const POSITION_VALUES: Record<string, number[][]> = {
  'R': [ // 车 - 优先占据中路
    [206, 208, 207, 213, 214, 213, 207, 208, 206],
    [206, 212, 209, 216, 233, 216, 209, 212, 206],
    [206, 208, 207, 214, 216, 214, 207, 208, 206],
    [206, 213, 213, 216, 216, 216, 213, 213, 206],
    [208, 211, 211, 214, 215, 214, 211, 211, 208],
    [208, 212, 212, 214, 215, 214, 212, 212, 208],
    [204, 209, 204, 212, 214, 212, 204, 209, 204],
    [198, 208, 204, 212, 212, 212, 204, 208, 198],
    [200, 208, 206, 212, 200, 212, 206, 208, 200],
    [194, 206, 204, 212, 200, 212, 204, 206, 194],
  ],
  'H': [ // 马 - 优先占据中心
    [90, 90, 90, 96, 90, 96, 90, 90, 90],
    [90, 96, 103, 97, 94, 97, 103, 96, 90],
    [92, 98, 99, 103, 99, 103, 99, 98, 92],
    [93, 108, 100, 107, 100, 107, 100, 108, 93],
    [90, 100, 99, 103, 104, 103, 99, 100, 90],
    [90, 98, 101, 102, 103, 102, 101, 98, 90],
    [92, 94, 98, 95, 98, 95, 98, 94, 92],
    [93, 92, 94, 95, 92, 95, 94, 92, 93],
    [85, 90, 92, 93, 78, 93, 92, 90, 85],
    [88, 85, 90, 88, 90, 88, 90, 85, 88],
  ],
  'C': [ // 炮 - 优先占据中路和河口
    [100, 100, 96, 91, 90, 91, 96, 100, 100],
    [98, 98, 96, 92, 89, 92, 96, 98, 98],
    [97, 97, 96, 91, 92, 91, 96, 97, 97],
    [96, 99, 99, 98, 100, 98, 99, 99, 96],
    [96, 96, 96, 96, 100, 96, 96, 96, 96],
    [95, 96, 99, 96, 100, 96, 99, 96, 95],
    [96, 96, 96, 96, 96, 96, 96, 96, 96],
    [97, 96, 100, 99, 101, 99, 100, 96, 97],
    [96, 97, 98, 98, 98, 98, 98, 97, 96],
    [96, 96, 97, 99, 99, 99, 97, 96, 96],
  ],
  'P': [ // 兵/卒 - 过河后价值大幅提升
    [9, 9, 9, 11, 13, 11, 9, 9, 9],
    [19, 24, 34, 42, 44, 42, 34, 24, 19],
    [19, 24, 32, 37, 37, 37, 32, 24, 19],
    [19, 23, 27, 29, 30, 29, 27, 23, 19],
    [14, 18, 20, 27, 29, 27, 20, 18, 14],
    [7, 0, 13, 0, 16, 0, 13, 0, 7],
    [7, 0, 7, 0, 15, 0, 7, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ],
};

// Evaluate a position from AI's perspective
function evaluatePosition(
  board: (Piece | null)[][],
  aiColor: 'red' | 'black'
): number {
  let score = 0;

  // 1. Material value (35% weight)
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      const piece = board[r]?.[c];
      if (piece) {
        const value = PIECE_VALUES[piece.type] || 0;
        if (piece.color === aiColor) {
          score += value;
        } else {
          score -= value;
        }
      }
    }
  }

  // 2. Position value (30% weight)
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      const piece = board[r]?.[c];
      if (piece && POSITION_VALUES[piece.type]) {
        // Flip row for black pieces
        const row = piece.color === aiColor ? r : 9 - r;
        const posValue = POSITION_VALUES[piece.type][row]?.[c] || 0;
        if (piece.color === aiColor) {
          score += posValue * 0.3;
        } else {
          score -= posValue * 0.3;
        }
      }
    }
  }

  // 3. King safety (15% weight)
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      const piece = board[r]?.[c];
      if (piece?.type === 'K') {
        // Count protection around king
        let protection = 0;
        for (let dr = -1; dr <= 1; dr++) {
          for (let dc = -1; dc <= 1; dc++) {
            if (dr === 0 && dc === 0) continue;
            const nr = r + dr;
            const nc = c + dc;
            if (nr >= 0 && nr < 10 && nc >= 0 && nc < 9) {
              const neighbor = board[nr]?.[nc];
              if (neighbor?.color === piece.color) {
                protection++;
              }
            }
          }
        }
        const safetyBonus = protection * 5;
        if (piece.color === aiColor) {
          score += safetyBonus;
        } else {
          score -= safetyBonus;
        }
      }
    }
  }

  // 4. Aggression (15% weight) - control enemy half
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      const piece = board[r]?.[c];
      if (piece) {
        const inEnemyHalf = aiColor === 'red' ? r <= 4 : r >= 5;
        if (inEnemyHalf) {
          let aggressionBonus = 15;
          if (piece.type === 'P') aggressionBonus = 30; // Pawns in enemy half are valuable
          if (piece.color === aiColor) {
            score += aggressionBonus;
          } else {
            score -= aggressionBonus;
          }
        }
      }
    }
  }

  // 5. Center control (10% weight)
  for (let r = 0; r < 10; r++) {
    for (let c = 3; c <= 5; c++) {
      const piece = board[r]?.[c];
      if (piece) {
        if (piece.color === aiColor) {
          score += 10;
        } else {
          score -= 10;
        }
      }
    }
  }

  return score;
}

// Alpha-Beta search with depth limit
function alphaBetaSearch(
  board: (Piece | null)[][],
  depth: number,
  alpha: number,
  beta: number,
  isMaximizing: boolean,
  aiColor: 'red' | 'black'
): number {
  // Terminal node - evaluate position
  if (depth === 0) {
    return evaluatePosition(board, aiColor);
  }

  const currentColor = isMaximizing ? aiColor : (aiColor === 'red' ? 'black' : 'red');
  const moves = getAllLegalMoves(board, currentColor);

  if (moves.length === 0) {
    // No legal moves - stalemate or checkmate
    return evaluatePosition(board, aiColor);
  }

  // Sort moves by heuristic (captures first, then aggressive moves)
  moves.sort((a, b) => {
    const aScore = getMoveScore(board, a, aiColor);
    const bScore = getMoveScore(board, b, aiColor);
    return bScore - aScore;
  });

  if (isMaximizing) {
    let maxEval = -Infinity;
    for (const move of moves) {
      const captured = board[move.to[0]][move.to[1]];
      board[move.to[0]][move.to[1]] = board[move.from[0]][move.from[1]];
      board[move.from[0]][move.from[1]] = null;

      const eval_ = alphaBetaSearch(board, depth - 1, alpha, beta, false, aiColor);

      board[move.from[0]][move.from[1]] = board[move.to[0]][move.to[1]];
      board[move.to[0]][move.to[1]] = captured;

      maxEval = Math.max(maxEval, eval_);
      alpha = Math.max(alpha, eval_);
      if (beta <= alpha) break; // Beta cutoff
    }
    return maxEval;
  } else {
    let minEval = Infinity;
    for (const move of moves) {
      const captured = board[move.to[0]][move.to[1]];
      board[move.to[0]][move.to[1]] = board[move.from[0]][move.from[1]];
      board[move.from[0]][move.from[1]] = null;

      const eval_ = alphaBetaSearch(board, depth - 1, alpha, beta, true, aiColor);

      board[move.from[0]][move.from[1]] = board[move.to[0]][move.to[1]];
      board[move.to[0]][move.to[1]] = captured;

      minEval = Math.min(minEval, eval_);
      beta = Math.min(beta, eval_);
      if (beta <= alpha) break; // Alpha cutoff
    }
    return minEval;
  }
}

// Get heuristic score for move ordering
function getMoveScore(
  board: (Piece | null)[][],
  move: { from: [number, number]; to: [number, number] },
  aiColor: 'red' | 'black'
): number {
  let score = 0;

  // Captures are high priority
  const target = board[move.to[0]][move.to[1]];
  if (target && target.color !== aiColor) {
    score += (PIECE_VALUES[target.type] || 0) * 10;
  }

  // Aggressive moves (moving into enemy half)
  if (aiColor === 'red' && move.to[0] <= 4) {
    score += 50;
  } else if (aiColor === 'black' && move.to[0] >= 5) {
    score += 50;
  }

  // Center control
  if (move.to[1] >= 3 && move.to[1] <= 5) {
    score += 30;
  }

  return score;
}

// Get all legal moves for a color
function getAllLegalMoves(
  board: (Piece | null)[][],
  color: 'red' | 'black'
): Array<{ from: [number, number]; to: [number, number] }> {
  const moves: Array<{ from: [number, number]; to: [number, number] }> = [];

  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      const piece = board[r]?.[c];
      if (piece && piece.color === color) {
        const pieceMoves = getLegalMovesForPiece(board, r, c);
        for (const [toR, toC] of pieceMoves) {
          moves.push({ from: [r, c], to: [toR, toC] });
        }
      }
    }
  }

  return moves;
}

// Get best move using Alpha-Beta search
function getBestAIMove(
  board: (Piece | null)[][],
  aiColor: 'red' | 'black',
  depth: number = 2
): { from: [number, number]; to: [number, number] } | null {
  const moves = getAllLegalMoves(board, aiColor);
  if (moves.length === 0) return null;

  let bestMove = moves[0];
  let bestScore = -Infinity;

  for (const move of moves) {
    const captured = board[move.to[0]][move.to[1]];
    board[move.to[0]][move.to[1]] = board[move.from[0]][move.from[1]];
    board[move.from[0]][move.from[1]] = null;

    const score = alphaBetaSearch(board, depth - 1, -Infinity, Infinity, false, aiColor);

    board[move.from[0]][move.from[1]] = board[move.to[0]][move.to[1]];
    board[move.to[0]][move.to[1]] = captured;

    if (score > bestScore) {
      bestScore = score;
      bestMove = move;
    }
  }

  return bestMove;
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
