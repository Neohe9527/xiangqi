/**
 * Game state hook for managing game logic
 */

import { useCallback } from 'react';
import { useGameStore } from '../stores/gameStore';
import { createGame, makeMove, requestAIMove, undoMove, getLegalMoves } from '../utils/api';
import type { AIType } from '../types/game';

export function useGameState() {
  const {
    gameId,
    gameState,
    selectedPiece,
    legalMoves,
    isLoading,
    isAIThinking,
    aiType,
    playerColor,
    setGameId,
    setGameState,
    setSelectedPiece,
    setLegalMoves,
    setIsLoading,
    setIsAIThinking,
    setThinkingInfo,
    setError,
    clearSelection,
    reset,
    getPiece,
    isPlayerTurn,
  } = useGameStore();

  const startNewGame = useCallback(async (newAIType?: AIType, newPlayerColor?: 'red' | 'black') => {
    setIsLoading(true);
    setError(null);
    reset();

    try {
      const result = await createGame(
        newAIType || aiType,
        newPlayerColor || playerColor
      );
      setGameId(result.game_id);
      setGameState(result.game_state);

      // If player is black, AI moves first
      if ((newPlayerColor || playerColor) === 'black') {
        await triggerAIMove(result.game_id);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start game');
    } finally {
      setIsLoading(false);
    }
  }, [aiType, playerColor]);

  const triggerAIMove = useCallback(async (gid?: string) => {
    const id = gid || gameId;
    if (!id) return;

    setIsAIThinking(true);
    setError(null);

    try {
      const result = await requestAIMove(id);
      setGameState(result.game_state);
      if (result.thinking_info) {
        setThinkingInfo(result.thinking_info as any);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'AI move failed');
    } finally {
      setIsAIThinking(false);
    }
  }, [gameId]);

  const handleCellClick = useCallback(async (row: number, col: number) => {
    if (!gameId || !gameState || gameState.game_result !== 'ongoing') return;
    if (isAIThinking || isLoading) return;
    if (!isPlayerTurn()) return;

    const clickedPiece = getPiece(row, col);

    // If no piece is selected
    if (!selectedPiece) {
      // Select player's piece
      if (clickedPiece && clickedPiece.color === playerColor) {
        setSelectedPiece({ row, col });
        try {
          const result = await getLegalMoves(gameId, row, col);
          setLegalMoves(result.legal_moves.map(([r, c]) => ({ row: r, col: c })));
        } catch (e) {
          console.error('Failed to get legal moves:', e);
        }
      }
      return;
    }

    // If clicking on the same piece, deselect
    if (selectedPiece.row === row && selectedPiece.col === col) {
      clearSelection();
      return;
    }

    // If clicking on another own piece, select it instead
    if (clickedPiece && clickedPiece.color === playerColor) {
      setSelectedPiece({ row, col });
      try {
        const result = await getLegalMoves(gameId, row, col);
        setLegalMoves(result.legal_moves.map(([r, c]) => ({ row: r, col: c })));
      } catch (e) {
        console.error('Failed to get legal moves:', e);
      }
      return;
    }

    // Check if this is a legal move
    const isLegalMove = legalMoves.some(m => m.row === row && m.col === col);
    if (!isLegalMove) {
      return;
    }

    // Make the move
    setIsLoading(true);
    try {
      const result = await makeMove(
        gameId,
        selectedPiece.row,
        selectedPiece.col,
        row,
        col
      );
      setGameState(result.game_state);
      clearSelection();

      // If game is still ongoing and it's AI's turn, trigger AI move
      if (result.game_state.game_result === 'ongoing' &&
          result.game_state.current_turn !== playerColor) {
        await triggerAIMove();
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Move failed');
    } finally {
      setIsLoading(false);
    }
  }, [gameId, gameState, selectedPiece, legalMoves, playerColor, isAIThinking, isLoading, isPlayerTurn, getPiece, triggerAIMove]);

  const handleUndo = useCallback(async () => {
    if (!gameId || isAIThinking || isLoading) return;

    setIsLoading(true);
    try {
      const result = await undoMove(gameId, 2);
      setGameState(result.game_state);
      clearSelection();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Undo failed');
    } finally {
      setIsLoading(false);
    }
  }, [gameId, isAIThinking, isLoading]);

  return {
    gameId,
    gameState,
    selectedPiece,
    legalMoves,
    isLoading,
    isAIThinking,
    startNewGame,
    handleCellClick,
    handleUndo,
    isPlayerTurn,
  };
}
