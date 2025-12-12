import React from 'react';
import { useGame } from '@/contexts/GameContext';
import { useAuth } from '@/contexts/AuthContext';
import { cn } from '@/lib/utils';
import { Timer, Axe, Trophy } from 'lucide-react';

const GameHUD: React.FC = () => {
  const { score, chops, timeLeft, gameState } = useGame();
  const { user } = useAuth();

  const timePercentage = (timeLeft / 10) * 100;
  const isLowTime = timeLeft <= 3;

  return (
    <div className="absolute top-4 left-4 right-4 flex justify-between items-start">
      {/* Left side - Score */}
      <div className="forest-card rounded-xl p-4 min-w-[120px]">
        <div className="flex items-center gap-2 text-muted-foreground text-sm mb-1">
          <Trophy className="w-4 h-4" />
          <span>Score</span>
        </div>
        <div
          data-testid="hud-score"
          className={cn(
            "text-3xl font-heading font-bold text-gradient-gold",
            gameState === 'playing' && "animate-score-pop"
          )}
        >
          {score}
        </div>
      </div>

      {/* Center - Timer */}
      <div className="forest-card rounded-xl p-4 min-w-[160px]">
        <div className="flex items-center gap-2 text-muted-foreground text-sm mb-2">
          <Timer className={cn("w-4 h-4", isLowTime && "text-destructive animate-pulse")} />
          <span>Time</span>
        </div>
        <div className="relative h-3 bg-muted rounded-full overflow-hidden">
          <div
            className={cn(
              "absolute inset-y-0 left-0 rounded-full transition-all duration-100",
              isLowTime
                ? "bg-gradient-to-r from-destructive to-destructive/70"
                : "bg-gradient-to-r from-primary to-gold"
            )}
            style={{ width: `${timePercentage}%` }}
          />
        </div>
        <div
          data-testid="hud-time"
          className={cn(
            "text-xl font-heading font-bold mt-1 text-center",
            isLowTime ? "text-destructive" : "text-foreground"
          )}
        >
          {timeLeft.toFixed(1)}s
        </div>
      </div>

      {/* Right side - Chops & User */}
      <div className="forest-card rounded-xl p-4 min-w-[120px] text-right">
        {user && (
          <div className="text-sm text-primary font-medium mb-2 truncate max-w-[100px]">
            {user.username}
          </div>
        )}
        <div className="flex items-center gap-2 text-muted-foreground text-sm mb-1 justify-end">
          <Axe className="w-4 h-4" />
          <span>Chops</span>
        </div>
        <div data-testid="hud-chops" className="text-2xl font-heading font-bold text-foreground">
          {chops}
        </div>
      </div>
    </div>
  );
};

export default GameHUD;