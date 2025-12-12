import React from 'react';
import { useGame, PlayerPosition } from '@/contexts/GameContext';
import { cn } from '@/lib/utils';

const Lumberjack: React.FC = () => {
  const { playerPosition, isChopping } = useGame();

  return (
    <div
      className={cn(
        "absolute bottom-8 transition-all duration-100",
        playerPosition === 'left' ? "left-8" : "right-8",
        playerPosition === 'right' && "scale-x-[-1]"
      )}
    >
      {/* Lumberjack character */}
      <div className="relative">
        {/* Body */}
        <div
          className="w-12 h-20 rounded-t-lg"
          style={{
            background: 'linear-gradient(180deg, hsl(0 70% 45%) 0%, hsl(0 60% 35%) 100%)',
          }}
        />
        
        {/* Head */}
        <div
          className="absolute -top-10 left-1/2 -translate-x-1/2 w-10 h-10 rounded-full"
          style={{
            background: 'linear-gradient(180deg, hsl(30 50% 70%) 0%, hsl(30 40% 55%) 100%)',
          }}
        >
          {/* Hat */}
          <div
            className="absolute -top-4 left-1/2 -translate-x-1/2 w-12 h-5 rounded-t-lg"
            style={{
              background: 'linear-gradient(180deg, hsl(25 50% 30%) 0%, hsl(25 45% 22%) 100%)',
            }}
          />
          
          {/* Eyes */}
          <div className="absolute top-3 left-2 w-1.5 h-1.5 rounded-full bg-primary-foreground" />
          <div className="absolute top-3 right-2 w-1.5 h-1.5 rounded-full bg-primary-foreground" />
        </div>

        {/* Arm with axe */}
        <div
          className={cn(
            "absolute top-2 -right-8 origin-bottom-left transition-transform",
            isChopping && "animate-chop"
          )}
        >
          {/* Arm */}
          <div
            className="w-3 h-10 rounded"
            style={{
              background: 'linear-gradient(90deg, hsl(0 70% 45%) 0%, hsl(0 60% 40%) 100%)',
            }}
          />
          
          {/* Axe handle */}
          <div
            className="absolute -top-8 left-1/2 -translate-x-1/2 w-2 h-12 rounded"
            style={{
              background: 'linear-gradient(180deg, hsl(30 40% 35%) 0%, hsl(30 35% 25%) 100%)',
            }}
          />
          
          {/* Axe head */}
          <div
            className="absolute -top-10 -left-3 w-8 h-6"
            style={{
              background: 'linear-gradient(135deg, hsl(220 10% 60%) 0%, hsl(220 10% 40%) 100%)',
              clipPath: 'polygon(30% 0%, 100% 0%, 100% 100%, 0% 100%)',
            }}
          />
        </div>

        {/* Legs */}
        <div className="flex gap-1 mt-1">
          <div
            className="w-5 h-8 rounded-b"
            style={{
              background: 'linear-gradient(180deg, hsl(220 30% 25%) 0%, hsl(220 25% 18%) 100%)',
            }}
          />
          <div
            className="w-5 h-8 rounded-b"
            style={{
              background: 'linear-gradient(180deg, hsl(220 30% 25%) 0%, hsl(220 25% 18%) 100%)',
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default Lumberjack;
