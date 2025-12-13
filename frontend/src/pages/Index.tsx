import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { api, LeaderboardEntry } from '@/services/api';
import { Button } from '@/components/ui/button';
import { Axe, Trophy, LogIn, LogOut, User, ChevronRight } from 'lucide-react';

const Index: React.FC = () => {
  const { user, isAuthenticated, logout, isLoading: authLoading } = useAuth();
  const [topPlayers, setTopPlayers] = useState<LeaderboardEntry[]>([]);

  useEffect(() => {
    const fetchTopPlayers = async () => {
      const response = await api.leaderboard.getLeaderboard(3);
      if (response.success) {
        setTopPlayers(response.entries);
      }
    };
    fetchTopPlayers();
  }, []);

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      {/* Background */}
      <div 
        className="fixed inset-0 -z-10"
        style={{
          background: 'linear-gradient(180deg, hsl(200 30% 15%) 0%, hsl(140 30% 12%) 40%, hsl(25 30% 10%) 100%)',
        }}
      >
        {/* Animated trees in background */}
        <div className="absolute bottom-0 left-0 right-0 h-64 overflow-hidden opacity-30">
          {[...Array(8)].map((_, i) => (
            <div
              key={i}
              className="absolute bottom-0"
              style={{
                left: `${i * 12.5}%`,
                width: '60px',
              }}
            >
              {/* Tree trunk */}
              <div 
                className="w-8 mx-auto"
                style={{
                  height: `${80 + Math.random() * 60}px`,
                  background: 'linear-gradient(90deg, hsl(25 50% 22%) 0%, hsl(25 50% 28%) 50%, hsl(25 50% 22%) 100%)',
                }}
              />
              {/* Tree top */}
              <div 
                className="absolute -top-12 left-1/2 -translate-x-1/2 w-16 h-16 rounded-full"
                style={{
                  background: 'radial-gradient(ellipse at center, hsl(120 40% 35%) 0%, hsl(120 40% 20%) 100%)',
                }}
              />
            </div>
          ))}
        </div>
      </div>

      {/* User status bar */}
      <div className="fixed top-4 right-4">
        {authLoading ? (
          <div className="forest-card rounded-lg px-4 py-2">
            <span className="text-muted-foreground">Loading...</span>
          </div>
        ) : isAuthenticated ? (
          <div className="forest-card rounded-lg px-4 py-2 flex items-center gap-3">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-primary" />
              <span className="font-heading font-semibold">{user?.username}</span>
            </div>
            <button 
              onClick={handleLogout}
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <Link to="/auth">
            <Button variant="outline" size="sm">
              <LogIn className="w-4 h-4 mr-2" />
              Sign In
            </Button>
          </Link>
        )}
      </div>

      {/* Main content */}
      <div className="text-center max-w-md mx-auto animate-slide-up">
        {/* Logo */}
        <div className="mb-8">
          <div className="inline-flex items-center justify-center w-24 h-24 rounded-2xl bg-gradient-to-br from-primary to-gold mb-4 animate-float shadow-lg">
            <Axe className="w-12 h-12 text-primary-foreground" />
          </div>
          <h1 className="text-5xl font-heading font-bold text-gradient-gold mb-2">
            Lumberjack
          </h1>
          <p className="text-lg text-muted-foreground">
            Chop fast. Dodge branches. Beat the clock!
          </p>
        </div>

        {/* Play button */}
        <Link to="/play" className="block mb-8">
          <Button variant="gold" size="xl" className="w-full animate-pulse-glow">
            <Axe className="w-6 h-6 mr-2" />
            Play Now
          </Button>
        </Link>

        {/* Stats card (if logged in) */}
        {isAuthenticated && user && (
          <div className="forest-card rounded-xl p-4 mb-6 text-left">
            <h3 className="font-heading font-semibold text-sm text-muted-foreground mb-3">
              Your Stats
            </h3>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-2xl font-heading font-bold text-gradient-gold">
                  {user.highScore}
                </p>
                <p className="text-xs text-muted-foreground">High Score</p>
              </div>
              <div>
                <p className="text-2xl font-heading font-bold text-foreground">
                  {user.totalChops.toLocaleString()}
                </p>
                <p className="text-xs text-muted-foreground">Total Chops</p>
              </div>
              <div>
                <p className="text-2xl font-heading font-bold text-foreground">
                  {user.gamesPlayed}
                </p>
                <p className="text-xs text-muted-foreground">Games</p>
              </div>
            </div>
          </div>
        )}

        {/* Top players preview */}
        <div className="forest-card rounded-xl p-4 text-left">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-heading font-semibold flex items-center gap-2">
              <Trophy className="w-4 h-4 text-gold" />
              Top Players
            </h3>
            <Link 
              to="/leaderboard" 
              className="text-sm text-primary hover:underline flex items-center gap-1"
            >
              View All
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
          
          <div className="space-y-2">
            {topPlayers.map((player, index) => (
              <div 
                key={player.id}
                className="flex items-center justify-between py-2 border-b border-border/50 last:border-0"
              >
                <div className="flex items-center gap-3">
                  <span className={`w-6 text-center font-bold ${
                    index === 0 ? 'text-gold' : 'text-muted-foreground'
                  }`}>
                    {index + 1}
                  </span>
                  <span className="font-medium">{player.username}</span>
                </div>
                <span className={`font-heading font-bold ${
                  index === 0 ? 'text-gradient-gold' : 'text-foreground'
                }`}>
                  {player.score.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-8 text-sm text-muted-foreground">
          <p>Use <strong>← / A</strong> and <strong>→ / D</strong> to chop and move</p>
        </div>
      </div>
    </div>
  );
};

export default Index;
