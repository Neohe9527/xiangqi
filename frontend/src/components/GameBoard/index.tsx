/**
 * Main GameBoard component
 */

import { BoardCanvas } from './BoardCanvas';
import { useGameStore } from '../../stores/gameStore';

interface GameBoardProps {
  onCellClick: (row: number, col: number) => void;
}

export function GameBoard({ onCellClick }: GameBoardProps) {
  const { gameState, selectedPiece, legalMoves, playerColor } = useGameStore();

  if (!gameState) {
    return (
      <div className="flex items-center justify-center w-full h-96 bg-amber-100 rounded-lg">
        <p className="text-gray-500 text-lg">点击"新游戏"开始</p>
      </div>
    );
  }

  return (
    <BoardCanvas
      board={gameState.board}
      selectedPiece={selectedPiece}
      legalMoves={legalMoves}
      lastMove={gameState.last_move}
      isCheck={gameState.is_check}
      currentTurn={gameState.current_turn}
      playerColor={playerColor}
      onCellClick={onCellClick}
    />
  );
}

export { BoardCanvas } from './BoardCanvas';
export * from './constants';
