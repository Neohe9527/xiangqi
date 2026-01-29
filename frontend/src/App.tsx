/**
 * Main App component
 */

import { useEffect } from 'react';
import { GameBoard } from './components/GameBoard';
import { InfoPanel } from './components/InfoPanel';
import { ControlPanel } from './components/ControlPanel';
import { GameOverDialog } from './components/Dialogs';
import { useGameState } from './hooks/useGameState';
import { useGameStore } from './stores/gameStore';

function App() {
  const {
    gameState,
    isLoading,
    isAIThinking,
    startNewGame,
    handleCellClick,
    handleUndo,
  } = useGameState();

  const { error, setError } = useGameStore();

  // Auto-start a game on first load
  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      {/* Header */}
      <header className="bg-amber-800 text-white py-4 shadow-lg">
        <div className="container mx-auto px-4">
          <h1 className="text-2xl md:text-3xl font-bold text-center">
            中国象棋
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <div className="flex flex-col lg:flex-row gap-6 justify-center items-start">
          {/* Game Board */}
          <div className="flex-shrink-0">
            <GameBoard onCellClick={handleCellClick} />
          </div>

          {/* Side Panel */}
          <div className="w-full lg:w-80 space-y-4">
            <ControlPanel
              onNewGame={startNewGame}
              onUndo={handleUndo}
              isLoading={isLoading}
              isAIThinking={isAIThinking}
            />
            <InfoPanel />
          </div>
        </div>

        {/* Error Toast */}
        {error && (
          <div className="fixed bottom-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-3">
            <span>{error}</span>
            <button
              onClick={() => setError(null)}
              className="text-white hover:text-red-200"
            >
              ✕
            </button>
          </div>
        )}
      </main>

      {/* Game Over Dialog */}
      {gameState?.game_result !== 'ongoing' && (
        <GameOverDialog onNewGame={() => startNewGame()} />
      )}

      {/* Footer */}
      <footer className="bg-amber-800 text-amber-200 py-3 mt-auto">
        <div className="container mx-auto px-4 text-center text-sm">
          <p>中国象棋 Web 版 | React + FastAPI</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
