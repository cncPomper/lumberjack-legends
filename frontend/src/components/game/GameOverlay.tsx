import React from 'react';
import { useGame } from '@/contexts/GameContext';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Play, RotateCcw, Trophy, Home, LogIn } from 'lucide-react';
import { Link } from 'react-router-dom';

const GameOverlay: React.FC = () => {
  const { gameState, score, chops, startGame } = useGame();
  const { user, isAuthenticated } = useAuth();

  if (gameState === 'playing') return null;

  return (
    <div className="absolute inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-20">
      <div className="forest-card rounded-2xl p-8 max-w-md w-full mx-4 text-center animate-slide-up">
        {gameState === 'idle' && (
          <>
            <h2 className="text-4xl font-heading font-bold text-gradient-gold mb-4">
              🪓 Lumberjack
            </h2>
            <p className="text-muted-foreground mb-6">
              Chop the tree as fast as you can!<br />
              Avoid the branches or you'll lose.
            </p>
            
            <div className="mb-6 p-4 bg-muted/30 rounded-lg">
              <h4 className="font-heading font-semibold mb-2">Controls</h4>
              <p className="text-sm text-muted-foreground">
                <strong>← / A</strong> - Chop Left<br />
                <strong>→ / D</strong> - Chop Right
              </p>
            </div>

            {isAuthenticated ? (
              <div className="mb-4 text-sm text-accent">
                Playing as <span className="font-bold">{user?.username}</span>
              </div>
            ) : (
              <div className="mb-4 text-sm text-muted-foreground">
                <Link to="/auth" className="text-primary hover:underline">
                  Sign in
                </Link>{' '}
                to save your scores!
              </div>
            )}

            <Button variant="gold" size="xl" className="w-full" onClick={startGame}>
              <Play className="w-6 h-6 mr-2" />
              Start Game
            </Button>
          </>
        )}

        {gameState === 'gameover' && (
          <>
            <h2 className="text-4xl font-heading font-bold text-destructive mb-2">
              Game Over!
            </h2>
            
            <div className="my-6 p-6 bg-muted/30 rounded-xl">
              <div className="flex items-center justify-center gap-2 mb-4">
                <Trophy className="w-8 h-8 text-gold" />
                <span className="text-5xl font-heading font-bold text-gradient-gold">
                  {score}
                </span>
              </div>
              <div className="text-muted-foreground">
                Total Chops: <span className="font-bold text-foreground">{chops}</span>
              </div>
            </div>

            {!isAuthenticated && (
              <div className="mb-4 p-3 bg-primary/10 rounded-lg text-sm">
                <Link to="/auth" className="text-primary font-medium hover:underline flex items-center justify-center gap-2">
                  <LogIn className="w-4 h-4" />
                  Sign in to save your score!
                </Link>
              </div>
            )}

            <div className="flex flex-col gap-3">
              <Button variant="gold" size="lg" className="w-full" onClick={startGame}>
                <RotateCcw className="w-5 h-5 mr-2" />
                Play Again
              </Button>
              
              <Link to="/leaderboard" className="w-full">
                <Button variant="outline" size="lg" className="w-full">
                  <Trophy className="w-5 h-5 mr-2" />
                  View Leaderboard
                </Button>
              </Link>
              
              <Link to="/" className="w-full">
                <Button variant="ghost" size="lg" className="w-full">
                  <Home className="w-5 h-5 mr-2" />
                  Back to Menu
                </Button>
              </Link>
            </div>
          </>
        )}

        {gameState === 'paused' && (
          <>
            <h2 className="text-3xl font-heading font-bold mb-6">Paused</h2>
            <Button variant="gold" size="lg" className="w-full">
              Resume
            </Button>
          </>
        )}
      </div>
    </div>
  );
};

export default GameOverlay;
