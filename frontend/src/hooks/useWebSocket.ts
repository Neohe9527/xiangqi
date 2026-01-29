/**
 * WebSocket hook for real-time game communication
 */

import { useEffect, useRef, useCallback } from 'react';
import { useGameStore } from '../stores/gameStore';
import { getWebSocketUrl } from '../utils/api';
import type { GameState, ThinkingInfo } from '../types/game';

interface WSMessage {
  type: string;
  data: unknown;
}

export function useWebSocket(gameId: string | null) {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const {
    setGameState,
    setIsAIThinking,
    setThinkingInfo,
    setError,
    clearSelection,
  } = useGameStore();

  const connect = useCallback(() => {
    if (!gameId) return;

    const ws = new WebSocket(getWebSocketUrl(gameId));

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const message: WSMessage = JSON.parse(event.data);
        handleMessage(message);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('Connection error');
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      // Attempt to reconnect after 3 seconds
      reconnectTimeoutRef.current = window.setTimeout(() => {
        if (gameId) {
          connect();
        }
      }, 3000);
    };

    wsRef.current = ws;
  }, [gameId]);

  const handleMessage = useCallback((message: WSMessage) => {
    switch (message.type) {
      case 'game_state':
        setGameState(message.data as GameState);
        break;

      case 'move_made':
        {
          const data = message.data as { game_state: GameState };
          setGameState(data.game_state);
          clearSelection();
        }
        break;

      case 'ai_thinking':
        setIsAIThinking(true);
        setThinkingInfo(null);
        break;

      case 'ai_move':
        {
          const data = message.data as {
            game_state: GameState;
            thinking_info?: ThinkingInfo;
          };
          setGameState(data.game_state);
          setIsAIThinking(false);
          if (data.thinking_info) {
            setThinkingInfo(data.thinking_info);
          }
        }
        break;

      case 'undo_done':
        {
          const data = message.data as { game_state: GameState };
          setGameState(data.game_state);
          clearSelection();
        }
        break;

      case 'legal_moves':
        // Handled by the component directly
        break;

      case 'error':
        {
          const data = message.data as { message: string };
          setError(data.message);
        }
        break;

      default:
        console.log('Unknown message type:', message.type);
    }
  }, [setGameState, setIsAIThinking, setThinkingInfo, setError, clearSelection]);

  const sendMessage = useCallback((message: WSMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  const sendMove = useCallback((fromRow: number, fromCol: number, toRow: number, toCol: number) => {
    sendMessage({
      type: 'move',
      data: { from_row: fromRow, from_col: fromCol, to_row: toRow, to_col: toCol },
    });
  }, [sendMessage]);

  const requestAIMove = useCallback(() => {
    sendMessage({ type: 'request_ai_move', data: {} });
  }, [sendMessage]);

  const requestUndo = useCallback((steps: number = 2) => {
    sendMessage({ type: 'undo', data: { steps } });
  }, [sendMessage]);

  const requestLegalMoves = useCallback((row: number, col: number) => {
    sendMessage({ type: 'get_legal_moves', data: { row, col } });
  }, [sendMessage]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  return {
    sendMove,
    requestAIMove,
    requestUndo,
    requestLegalMoves,
    isConnected: wsRef.current?.readyState === WebSocket.OPEN,
  };
}
