import React from 'react';
import { GameProvider } from '@/contexts/GameContext';
import GameArena from '@/components/game/GameArena';

const GamePage: React.FC = () => {
  return (
    <GameProvider>
      <GameArena />
    </GameProvider>
  );
};

export default GamePage;
