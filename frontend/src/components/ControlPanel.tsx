/**
 * Control panel with game actions
 */

import { useState } from 'react';
import { useGameStore } from '../stores/gameStore';
import type { AIType } from '../types/game';

interface ControlPanelProps {
  onNewGame: (aiType?: AIType, playerColor?: 'red' | 'black') => void;
  onUndo: () => void;
  isLoading: boolean;
  isAIThinking: boolean;
}

const AI_OPTIONS: { value: AIType; label: string; description: string }[] = [
  { value: 'random', label: '新手小卒', description: '随机走子' },
  { value: 'greedy', label: '贪心将军', description: '优先吃子' },
  { value: 'minimax', label: '谋略军师', description: '有战术深度' },
  { value: 'alphabeta', label: '深算国手', description: '最强AI' },
];

export function ControlPanel({ onNewGame, onUndo, isLoading, isAIThinking }: ControlPanelProps) {
  const { gameState, aiType, playerColor, setAIType, setPlayerColor } = useGameStore();
  const [showSettings, setShowSettings] = useState(false);

  const canUndo = gameState && gameState.game_result === 'ongoing' && gameState.move_count >= 2;
  const isDisabled = isLoading || isAIThinking;

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 space-y-4">
      {/* Main Actions */}
      <div className="space-y-2">
        <button
          onClick={() => onNewGame()}
          disabled={isDisabled}
          className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors"
        >
          {isLoading ? '加载中...' : '新游戏'}
        </button>

        <button
          onClick={onUndo}
          disabled={isDisabled || !canUndo}
          className="w-full py-2 px-4 bg-amber-500 hover:bg-amber-600 disabled:bg-gray-300 text-white font-medium rounded-lg transition-colors"
        >
          悔棋
        </button>
      </div>

      {/* Settings Toggle */}
      <button
        onClick={() => setShowSettings(!showSettings)}
        className="w-full py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
      >
        <span>游戏设置</span>
        <span className={`transform transition-transform ${showSettings ? 'rotate-180' : ''}`}>
          ▼
        </span>
      </button>

      {/* Settings Panel */}
      {showSettings && (
        <div className="space-y-4 pt-2 border-t">
          {/* AI Difficulty */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              AI难度
            </label>
            <div className="space-y-2">
              {AI_OPTIONS.map((option) => (
                <label
                  key={option.value}
                  className={`flex items-center p-2 rounded-lg cursor-pointer transition-colors ${
                    aiType === option.value
                      ? 'bg-blue-50 border-2 border-blue-500'
                      : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                  }`}
                >
                  <input
                    type="radio"
                    name="aiType"
                    value={option.value}
                    checked={aiType === option.value}
                    onChange={(e) => setAIType(e.target.value as AIType)}
                    className="sr-only"
                  />
                  <div className="flex-1">
                    <div className="font-medium text-gray-800">{option.label}</div>
                    <div className="text-xs text-gray-500">{option.description}</div>
                  </div>
                  {aiType === option.value && (
                    <span className="text-blue-500">✓</span>
                  )}
                </label>
              ))}
            </div>
          </div>

          {/* Player Color */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              执子颜色
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => setPlayerColor('red')}
                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                  playerColor === 'red'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                红方 (先手)
              </button>
              <button
                onClick={() => setPlayerColor('black')}
                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                  playerColor === 'black'
                    ? 'bg-gray-800 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                黑方 (后手)
              </button>
            </div>
          </div>

          {/* Apply Settings */}
          <button
            onClick={() => {
              onNewGame(aiType, playerColor);
              setShowSettings(false);
            }}
            disabled={isDisabled}
            className="w-full py-2 px-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors"
          >
            应用设置并开始新游戏
          </button>
        </div>
      )}

      {/* AI Thinking Indicator */}
      {isAIThinking && (
        <div className="flex items-center justify-center gap-2 py-2 text-blue-600">
          <div className="animate-spin h-5 w-5 border-2 border-blue-600 border-t-transparent rounded-full"></div>
          <span>AI思考中...</span>
        </div>
      )}
    </div>
  );
}
