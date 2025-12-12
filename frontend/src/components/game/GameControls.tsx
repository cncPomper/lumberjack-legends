import React, { useEffect, useCallback } from 'react';
import { useGame } from '@/contexts/GameContext';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const GameControls: React.FC = () => {
  const { gameState, playerPosition, chop, movePlayer } = useGame();

  const handleChop = useCallback(() => {
    if (gameState === 'playing') {
      chop();
    }
  }, [gameState, chop]);

  const handleMoveLeft = useCallback(() => {
    if (playerPosition !== 'left') {
      movePlayer('left');
    }
    handleChop();
  }, [playerPosition, movePlayer, handleChop]);

  const handleMoveRight = useCallback(() => {
    if (playerPosition !== 'right') {
      movePlayer('right');
    }
    handleChop();
  }, [playerPosition, movePlayer, handleChop]);

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (gameState !== 'playing') return;

      switch (e.key) {
        case 'ArrowLeft':
        case 'a':
        case 'A':
          handleMoveLeft();
          break;
        case 'ArrowRight':
        case 'd':
        case 'D':
          handleMoveRight();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [gameState, handleMoveLeft, handleMoveRight]);

  if (gameState !== 'playing') return null;

  return (
    <div className="absolute bottom-8 left-0 right-0 flex justify-center gap-8 px-4">
      <Button
        variant="game"
        size="xl"
        className="w-24 h-24 rounded-2xl"
        onClick={handleMoveLeft}
        aria-label="Move left and chop"
      >
        <ChevronLeft className="w-10 h-10" />
      </Button>
      
      <Button
        variant="game"
        size="xl"
        className="w-24 h-24 rounded-2xl"
        onClick={handleMoveRight}
        aria-label="Move right and chop"
      >
        <ChevronRight className="w-10 h-10" />
      </Button>
    </div>
  );
};

export default GameControls;
