import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, LeaderboardEntry } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Trophy, Medal, ArrowLeft, Crown, Axe, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

const LeaderboardPage: React.FC = () => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [userRank, setUserRank] = useState<number | undefined>();
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchLeaderboard = async () => {
      setIsLoading(true);
      const response = await api.leaderboard.getLeaderboard(10);
      if (response.success) {
        setEntries(response.entries);
        setUserRank(response.userRank);
      }
      setIsLoading(false);
    };

    fetchLeaderboard();
  }, []);

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Crown className="w-6 h-6 text-gold" />;
      case 2:
        return <Medal className="w-6 h-6 text-muted-foreground" style={{ color: 'hsl(45 10% 65%)' }} />;
      case 3:
        return <Medal className="w-6 h-6" style={{ color: 'hsl(25 60% 50%)' }} />;
      default:
        return <span className="w-6 text-center font-bold text-muted-foreground">{rank}</span>;
    }
  };

  const getRankStyle = (rank: number) => {
    switch (rank) {
      case 1:
        return 'bg-gradient-to-r from-gold/20 to-gold-glow/10 border-gold/30';
      case 2:
        return 'bg-muted/50 border-muted-foreground/20';
      case 3:
        return 'bg-gradient-to-r from-amber-900/20 to-transparent border-amber-700/20';
      default:
        return 'bg-card/50 border-border/50';
    }
  };

  return (
    <div className="min-h-screen p-4 pb-24">
      {/* Background */}
      <div 
        className="fixed inset-0 -z-10"
        style={{
          background: 'linear-gradient(180deg, hsl(200 30% 15%) 0%, hsl(140 30% 12%) 40%, hsl(25 30% 10%) 100%)',
        }}
      />

      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link 
            to="/" 
            className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </Link>

          <div className="flex items-center gap-2">
            <Trophy className="w-6 h-6 text-gold" />
            <h1 className="text-2xl font-heading font-bold text-gradient-gold">
              Leaderboard
            </h1>
          </div>

          <div className="w-16" />
        </div>

        {/* User rank card */}
        {user && userRank && (
          <div className="forest-card rounded-xl p-4 mb-6 animate-slide-up">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                  <Axe className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <p className="font-heading font-semibold">{user.username}</p>
                  <p className="text-sm text-muted-foreground">Your rank</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-3xl font-heading font-bold text-gradient-gold">#{userRank}</p>
                <p className="text-sm text-muted-foreground">{user.highScore} pts</p>
              </div>
            </div>
          </div>
        )}

        {/* Leaderboard list */}
        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        ) : (
          <div className="space-y-3">
            {entries.map((entry, index) => (
              <div
                key={entry.id}
                className={cn(
                  "forest-card rounded-xl p-4 border-2 transition-all animate-slide-up",
                  getRankStyle(entry.rank),
                  user?.id === entry.id && "ring-2 ring-primary"
                )}
                style={{ animationDelay: `${index * 50}ms` }}
              >
                <div className="flex items-center gap-4">
                  {/* Rank */}
                  <div className="w-8 flex items-center justify-center">
                    {getRankIcon(entry.rank)}
                  </div>

                  {/* User info */}
                  <div className="flex-1">
                    <p className={cn(
                      "font-heading font-semibold",
                      entry.rank === 1 && "text-gold"
                    )}>
                      {entry.username}
                      {user?.id === entry.id && (
                        <span className="ml-2 text-xs text-primary">(You)</span>
                      )}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {entry.chops.toLocaleString()} chops
                    </p>
                  </div>

                  {/* Score */}
                  <div className="text-right">
                    <p className={cn(
                      "text-2xl font-heading font-bold",
                      entry.rank === 1 ? "text-gradient-gold" : "text-foreground"
                    )}>
                      {entry.score.toLocaleString()}
                    </p>
                    <p className="text-xs text-muted-foreground">points</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Play button */}
        <div className="fixed bottom-6 left-4 right-4 max-w-2xl mx-auto">
          <Link to="/play">
            <Button variant="gold" size="xl" className="w-full">
              <Axe className="w-5 h-5 mr-2" />
              Play Now
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LeaderboardPage;
