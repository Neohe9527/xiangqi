/**
 * API utility functions
 */

import type { GameState, AIType, AIConfig } from '../types/game';

const API_BASE = '/api/v1';

export async function createGame(
  aiType: AIType = 'alphabeta',
  playerColor: 'red' | 'black' = 'red'
): Promise<{ game_id: string; game_state: GameState; ai_config: AIConfig }> {
  const response = await fetch(`${API_BASE}/games`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ai_type: aiType, player_color: playerColor }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create game');
  }

  return response.json();
}

export async function getGame(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE}/games/${gameId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get game');
  }

  return response.json();
}

export async function makeMove(
  gameId: string,
  fromRow: number,
  fromCol: number,
  toRow: number,
  toCol: number
): Promise<{ success: boolean; move_info: unknown; game_state: GameState }> {
  const response = await fetch(`${API_BASE}/games/${gameId}/moves`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from_row: fromRow,
      from_col: fromCol,
      to_row: toRow,
      to_col: toCol,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to make move');
  }

  return response.json();
}

export async function requestAIMove(
  gameId: string
): Promise<{ success: boolean; move_info: unknown; thinking_info: unknown; game_state: GameState }> {
  const response = await fetch(`${API_BASE}/games/${gameId}/ai-move`, {
    method: 'POST',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get AI move');
  }

  return response.json();
}

export async function undoMove(
  gameId: string,
  steps: number = 2
): Promise<{ success: boolean; game_state: GameState }> {
  const response = await fetch(`${API_BASE}/games/${gameId}/undo`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ steps }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to undo move');
  }

  return response.json();
}

export async function getLegalMoves(
  gameId: string,
  row: number,
  col: number
): Promise<{ legal_moves: [number, number][] }> {
  const response = await fetch(`${API_BASE}/games/${gameId}/legal-moves`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ row, col }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get legal moves');
  }

  return response.json();
}

export async function getAITypes(): Promise<Record<string, AIConfig>> {
  const response = await fetch(`${API_BASE}/games/config/ai-types`);

  if (!response.ok) {
    throw new Error('Failed to get AI types');
  }

  return response.json();
}

export function getWebSocketUrl(gameId: string): string {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  return `${protocol}//${host}/ws/games/${gameId}`;
}
