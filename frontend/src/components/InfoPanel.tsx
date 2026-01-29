/**
 * Information panel showing game status
 */

import { useGameStore } from '../stores/gameStore';

const AI_NAMES: Record<string, string> = {
  random: '新手小卒',
  greedy: '贪心将军',
  minimax: '谋略军师',
  alphabeta: '深算国手',
};

export function InfoPanel() {
  const { gameState, isAIThinking, thinkingInfo, aiType, playerColor } = useGameStore();

  if (!gameState) {
    return null;
  }

  const getStatusText = () => {
    if (gameState.game_result === 'red_win') {
      return { text: '红方胜利！', color: 'text-red-600' };
    }
    if (gameState.game_result === 'black_win') {
      return { text: '黑方胜利！', color: 'text-gray-800' };
    }
    if (gameState.game_result === 'draw') {
      return { text: '和棋', color: 'text-yellow-600' };
    }

    if (isAIThinking) {
      return { text: 'AI思考中...', color: 'text-blue-600' };
    }

    const turnText = gameState.current_turn === 'red' ? '红方' : '黑方';
    const isPlayerTurn = gameState.current_turn === playerColor;

    if (isPlayerTurn) {
      return { text: `${turnText}走棋 (你)`, color: gameState.current_turn === 'red' ? 'text-red-600' : 'text-gray-800' };
    } else {
      return { text: `${turnText}走棋 (AI)`, color: gameState.current_turn === 'red' ? 'text-red-600' : 'text-gray-800' };
    }
  };

  const status = getStatusText();

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 space-y-4">
      {/* Game Status */}
      <div className="text-center">
        <h2 className={`text-2xl font-bold ${status.color}`}>
          {status.text}
        </h2>
        {gameState.is_check && gameState.game_result === 'ongoing' && (
          <p className="text-red-500 font-semibold mt-1">将军！</p>
        )}
      </div>

      {/* Game Info */}
      <div className="border-t pt-4 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">回合数</span>
          <span className="font-medium">{Math.floor(gameState.move_count / 2) + 1}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">AI难度</span>
          <span className="font-medium">{AI_NAMES[aiType] || aiType}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">你执</span>
          <span className={`font-medium ${playerColor === 'red' ? 'text-red-600' : 'text-gray-800'}`}>
            {playerColor === 'red' ? '红方' : '黑方'}
          </span>
        </div>
      </div>

      {/* AI Thinking Info */}
      {thinkingInfo && (
        <div className="border-t pt-4">
          <h3 className="text-sm font-semibold text-gray-600 mb-2">AI思考信息</h3>
          <div className="space-y-1 text-xs text-gray-500">
            <div className="flex justify-between">
              <span>搜索深度</span>
              <span>{thinkingInfo.depth}</span>
            </div>
            <div className="flex justify-between">
              <span>评估节点</span>
              <span>{thinkingInfo.nodes_evaluated.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>评分</span>
              <span>{thinkingInfo.score.toFixed(0)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Captured Pieces */}
      {gameState.captured_pieces.length > 0 && (
        <div className="border-t pt-4">
          <h3 className="text-sm font-semibold text-gray-600 mb-2">被吃棋子</h3>
          <div className="flex flex-wrap gap-1">
            {gameState.captured_pieces.map((piece, index) => (
              <span
                key={index}
                className={`text-lg ${piece.color === 'red' ? 'text-red-600' : 'text-gray-800'}`}
              >
                {getPieceName(piece.type, piece.color)}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function getPieceName(type: string, color: string): string {
  const names: Record<string, Record<string, string>> = {
    red: { K: '帅', A: '仕', E: '相', H: '马', R: '车', C: '炮', P: '兵' },
    black: { K: '将', A: '士', E: '象', H: '马', R: '车', C: '炮', P: '卒' },
  };
  return names[color]?.[type] || '?';
}
