/**
 * Mock API for demonstration when backend is not available
 */

import type { GameState, AIType, AIConfig } from '../types/game';

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
        const moves: [number, number][] = [];
        if (row + 1 < 10) moves.push([row + 1, col]);
        if (col + 1 < 9) moves.push([row, col + 1]);
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
