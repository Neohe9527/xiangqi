/**
 * Game state management with Zustand
 */

import { create } from 'zustand';
import type { GameState, Piece, Position, AIType, ThinkingInfo } from '../types/game';

interface GameStore {
  // Game state
  gameId: string | null;
  gameState: GameState | null;

  // UI state
  selectedPiece: Position | null;
  legalMoves: Position[];
  isLoading: boolean;
  isAIThinking: boolean;
  thinkingInfo: ThinkingInfo | null;
  error: string | null;

  // Settings
  aiType: AIType;
  playerColor: 'red' | 'black';

  // Actions
  setGameId: (id: string | null) => void;
  setGameState: (state: GameState | null) => void;
  setSelectedPiece: (pos: Position | null) => void;
  setLegalMoves: (moves: Position[]) => void;
  setIsLoading: (loading: boolean) => void;
  setIsAIThinking: (thinking: boolean) => void;
  setThinkingInfo: (info: ThinkingInfo | null) => void;
  setError: (error: string | null) => void;
  setAIType: (type: AIType) => void;
  setPlayerColor: (color: 'red' | 'black') => void;

  // Computed helpers
  getPiece: (row: number, col: number) => Piece | null;
  isPlayerTurn: () => boolean;
  clearSelection: () => void;
  reset: () => void;
}

export const useGameStore = create<GameStore>((set, get) => ({
  // Initial state
  gameId: null,
  gameState: null,
  selectedPiece: null,
  legalMoves: [],
  isLoading: false,
  isAIThinking: false,
  thinkingInfo: null,
  error: null,
  aiType: 'alphabeta',
  playerColor: 'red',

  // Actions
  setGameId: (id) => set({ gameId: id }),
  setGameState: (state) => set({ gameState: state }),
  setSelectedPiece: (pos) => set({ selectedPiece: pos }),
  setLegalMoves: (moves) => set({ legalMoves: moves }),
  setIsLoading: (loading) => set({ isLoading: loading }),
  setIsAIThinking: (thinking) => set({ isAIThinking: thinking }),
  setThinkingInfo: (info) => set({ thinkingInfo: info }),
  setError: (error) => set({ error: error }),
  setAIType: (type) => set({ aiType: type }),
  setPlayerColor: (color) => set({ playerColor: color }),

  // Helpers
  getPiece: (row, col) => {
    const { gameState } = get();
    if (!gameState || !gameState.board) return null;
    return gameState.board[row]?.[col] || null;
  },

  isPlayerTurn: () => {
    const { gameState, playerColor } = get();
    if (!gameState) return false;
    return gameState.current_turn === playerColor;
  },

  clearSelection: () => set({ selectedPiece: null, legalMoves: [] }),

  reset: () => set({
    gameId: null,
    gameState: null,
    selectedPiece: null,
    legalMoves: [],
    isLoading: false,
    isAIThinking: false,
    thinkingInfo: null,
    error: null,
  }),
}));
