import React from 'react';
import Tree from './Tree';
import Lumberjack from './Lumberjack';
import GameHUD from './GameHUD';
import GameControls from './GameControls';
import GameOverlay from './GameOverlay';

const GameArena: React.FC = () => {
  return (
    <div className="relative w-full h-screen overflow-hidden">
      {/* Background */}
      <div 
        className="absolute inset-0"
        style={{
          background: 'linear-gradient(180deg, hsl(200 30% 15%) 0%, hsl(140 30% 12%) 40%, hsl(25 30% 10%) 100%)',
        }}
      >
        {/* Stars */}
        <div className="absolute inset-0 opacity-30">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-foreground rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 40}%`,
                opacity: Math.random() * 0.5 + 0.3,
                animation: `pulse-glow ${2 + Math.random() * 2}s ease-in-out infinite`,
                animationDelay: `${Math.random() * 2}s`,
              }}
            />
          ))}
        </div>

        {/* Moon */}
        <div 
          className="absolute top-10 right-20 w-16 h-16 rounded-full"
          style={{
            background: 'radial-gradient(circle at 30% 30%, hsl(45 20% 90%) 0%, hsl(45 15% 70%) 100%)',
            boxShadow: '0 0 40px hsl(45 20% 70% / 0.3)',
          }}
        />

        {/* Ground */}
        <div 
          className="absolute bottom-0 left-0 right-0 h-32"
          style={{
            background: 'linear-gradient(180deg, hsl(25 40% 15%) 0%, hsl(25 35% 10%) 100%)',
          }}
        >
          {/* Grass */}
          <div className="absolute top-0 left-0 right-0 h-4 overflow-hidden">
            {[...Array(40)].map((_, i) => (
              <div
                key={i}
                className="absolute bottom-0"
                style={{
                  left: `${i * 2.5}%`,
                  width: '8px',
                  height: `${10 + Math.random() * 15}px`,
                  background: 'linear-gradient(180deg, hsl(100 40% 30%) 0%, hsl(120 35% 20%) 100%)',
                  transform: `rotate(${-5 + Math.random() * 10}deg)`,
                  borderRadius: '2px 2px 0 0',
                }}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Game HUD */}
      <GameHUD />

      {/* Tree centered */}
      <div className="absolute bottom-32 left-1/2 -translate-x-1/2">
        <Tree />
      </div>

      {/* Lumberjack */}
      <div className="absolute bottom-32 left-1/2 -translate-x-1/2 w-64">
        <Lumberjack />
      </div>

      {/* Controls */}
      <GameControls />

      {/* Overlay for start/end screens */}
      <GameOverlay />
    </div>
  );
};

export default GameArena;
