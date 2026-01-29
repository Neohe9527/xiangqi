/**
 * Game over dialog
 */

import { useGameStore } from '../../stores/gameStore';

interface GameOverDialogProps {
  onNewGame: () => void;
}

export function GameOverDialog({ onNewGame }: GameOverDialogProps) {
  const { gameState, playerColor } = useGameStore();

  if (!gameState || gameState.game_result === 'ongoing') {
    return null;
  }

  const getResultInfo = () => {
    const isPlayerRed = playerColor === 'red';

    if (gameState.game_result === 'red_win') {
      return {
        title: '红方胜利！',
        subtitle: isPlayerRed ? '恭喜你赢了！' : 'AI获胜',
        color: 'text-red-600',
        bgColor: 'bg-red-50',
        isWin: isPlayerRed,
      };
    }

    if (gameState.game_result === 'black_win') {
      return {
        title: '黑方胜利！',
        subtitle: !isPlayerRed ? '恭喜你赢了！' : 'AI获胜',
        color: 'text-gray-800',
        bgColor: 'bg-gray-100',
        isWin: !isPlayerRed,
      };
    }

    return {
      title: '和棋',
      subtitle: '势均力敌',
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
      isWin: false,
    };
  };

  const result = getResultInfo();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className={`${result.bgColor} rounded-2xl shadow-2xl p-8 max-w-sm w-full mx-4 text-center transform animate-bounce-in`}>
        {/* Result Icon */}
        <div className="text-6xl mb-4">
          {result.isWin ? '🎉' : gameState.game_result === 'draw' ? '🤝' : '😔'}
        </div>

        {/* Title */}
        <h2 className={`text-3xl font-bold ${result.color} mb-2`}>
          {result.title}
        </h2>

        {/* Subtitle */}
        <p className="text-gray-600 mb-6">
          {result.subtitle}
        </p>

        {/* Stats */}
        <div className="bg-white rounded-lg p-4 mb-6">
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">总回合数</span>
            <span className="font-medium">{Math.floor(gameState.move_count / 2) + 1}</span>
          </div>
        </div>

        {/* Actions */}
        <button
          onClick={onNewGame}
          className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
        >
          再来一局
        </button>
      </div>
    </div>
  );
}
