import { describe, it, expect, beforeEach } from 'vitest';
import { api, mockAuthApi, mockLeaderboardApi, mockGameApi } from './mockApi';

describe('Mock API Service', () => {
  beforeEach(async () => {
    // Reset auth state before each test
    await mockAuthApi.logout();
  });

  describe('Authentication API', () => {
    describe('signup', () => {
      it('should create a new user with valid credentials', async () => {
        const result = await mockAuthApi.signup('TestUser123', 'test123@example.com', 'password123');
        
        expect(result.success).toBe(true);
        expect(result.user).toBeDefined();
        expect(result.user?.username).toBe('TestUser123');
        expect(result.user?.email).toBe('test123@example.com');
        expect(result.token).toBeDefined();
      });

      it('should reject signup with short username', async () => {
        const result = await mockAuthApi.signup('AB', 'short@test.com', 'password123');
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('Username must be at least 3 characters');
      });

      it('should reject signup with invalid email', async () => {
        const result = await mockAuthApi.signup('ValidUser', 'invalid-email', 'password123');
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('valid email');
      });

      it('should reject signup with short password', async () => {
        const result = await mockAuthApi.signup('ValidUser', 'valid@email.com', '123');
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('Password must be at least 6 characters');
      });

      it('should reject duplicate email', async () => {
        const result = await mockAuthApi.signup('NewUser', 'king@forest.com', 'password123');
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('Email already registered');
      });

      it('should reject duplicate username', async () => {
        const result = await mockAuthApi.signup('ForestKing', 'new@email.com', 'password123');
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('Username already taken');
      });
    });

    describe('login', () => {
      it('should login existing user with correct credentials', async () => {
        const result = await mockAuthApi.login('king@forest.com', 'password');
        
        expect(result.success).toBe(true);
        expect(result.user?.username).toBe('ForestKing');
        expect(result.token).toBeDefined();
      });

      it('should reject login with wrong email', async () => {
        const result = await mockAuthApi.login('wrong@email.com', 'password');
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('Invalid email or password');
      });

      it('should reject login with empty credentials', async () => {
        const result = await mockAuthApi.login('', '');
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('required');
      });
    });

    describe('logout', () => {
      it('should successfully logout', async () => {
        await mockAuthApi.login('king@forest.com', 'password');
        const result = await mockAuthApi.logout();
        
        expect(result.success).toBe(true);
        
        const userCheck = await mockAuthApi.getCurrentUser();
        expect(userCheck.success).toBe(false);
      });
    });

    describe('getCurrentUser', () => {
      it('should return current user when logged in', async () => {
        await mockAuthApi.login('king@forest.com', 'password');
        const result = await mockAuthApi.getCurrentUser();
        
        expect(result.success).toBe(true);
        expect(result.user?.username).toBe('ForestKing');
      });

      it('should return error when not logged in', async () => {
        const result = await mockAuthApi.getCurrentUser();
        
        expect(result.success).toBe(false);
        expect(result.error).toContain('Not authenticated');
      });
    });
  });

  describe('Leaderboard API', () => {
    describe('getLeaderboard', () => {
      it('should return sorted leaderboard entries', async () => {
        const result = await mockLeaderboardApi.getLeaderboard(5);
        
        expect(result.success).toBe(true);
        expect(result.entries.length).toBeLessThanOrEqual(5);
        expect(result.entries[0].rank).toBe(1);
        
        // Verify sorting
        for (let i = 1; i < result.entries.length; i++) {
          expect(result.entries[i].score).toBeLessThanOrEqual(result.entries[i - 1].score);
        }
      });

      it('should include user rank when logged in', async () => {
        await mockAuthApi.login('king@forest.com', 'password');
        const result = await mockLeaderboardApi.getLeaderboard();
        
        expect(result.userRank).toBeDefined();
        expect(result.userRank).toBeGreaterThan(0);
      });
    });

    describe('submitScore', () => {
      it('should update high score if new score is higher', async () => {
        await mockAuthApi.signup('ScoreTest', 'score@test.com', 'password123');
        const initialUser = await mockAuthApi.getCurrentUser();
        const initialScore = initialUser.user?.highScore || 0;
        
        await mockLeaderboardApi.submitScore(1000, 50);
        
        const updatedUser = await mockAuthApi.getCurrentUser();
        expect(updatedUser.user?.highScore).toBeGreaterThan(initialScore);
      });

      it('should increment games played', async () => {
        await mockAuthApi.signup('GamesTest', 'games@test.com', 'password123');
        const initialUser = await mockAuthApi.getCurrentUser();
        const initialGames = initialUser.user?.gamesPlayed || 0;
        
        await mockLeaderboardApi.submitScore(500, 25);
        
        const updatedUser = await mockAuthApi.getCurrentUser();
        expect(updatedUser.user?.gamesPlayed).toBe(initialGames + 1);
      });
    });
  });

  describe('Game API', () => {
    describe('startSession', () => {
      it('should create a new game session', async () => {
        const result = await mockGameApi.startSession();
        
        expect(result.success).toBe(true);
        expect(result.session).toBeDefined();
        expect(result.session?.id).toBeDefined();
        expect(result.session?.score).toBe(0);
        expect(result.session?.chops).toBe(0);
      });
    });

    describe('endSession', () => {
      it('should end session with stats', async () => {
        const startResult = await mockGameApi.startSession();
        const sessionId = startResult.session!.id;
        
        const result = await mockGameApi.endSession(sessionId, 500, 100, 60);
        
        expect(result.success).toBe(true);
        expect(result.session?.score).toBe(500);
        expect(result.session?.chops).toBe(100);
        expect(result.session?.endedAt).toBeDefined();
      });
    });

    describe('getStats', () => {
      it('should return stats for logged in user', async () => {
        await mockAuthApi.login('king@forest.com', 'password');
        const result = await mockGameApi.getStats();
        
        expect(result.success).toBe(true);
        expect(result.stats).toBeDefined();
        expect(result.stats?.totalGames).toBeGreaterThan(0);
      });

      it('should fail for non-authenticated users', async () => {
        const result = await mockGameApi.getStats();
        
        expect(result.success).toBe(false);
      });
    });
  });
});
