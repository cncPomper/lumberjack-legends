// API Service for Lumberjack Game - Real Backend Integration
// Connects to FastAPI backend based on OpenAPI specification

export interface User {
  id: string;
  username: string;
  email: string;
  createdAt: Date;
  highScore: number;
  totalChops: number;
  gamesPlayed: number;
}

export interface LeaderboardEntry {
  id: string;
  username: string;
  score: number;
  chops: number;
  rank: number;
  timestamp: Date;
}

export interface GameSession {
  id: string;
  userId: string;
  score: number;
  chops: number;
  duration: number;
  startedAt: Date;
  endedAt?: Date;
}

export interface AuthResponse {
  success: boolean;
  user?: User;
  token?: string;
  error?: string;
}

export interface LeaderboardResponse {
  success: boolean;
  entries: LeaderboardEntry[];
  userRank?: number;
  error?: string;
}

export interface GameSessionResponse {
  success: boolean;
  session?: GameSession;
  error?: string;
}

// Get API base URL from environment or use default
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

// Storage for auth token
let authToken: string | null = localStorage.getItem('authToken');

// Helper to set auth token
const setAuthToken = (token: string | null) => {
  authToken = token;
  if (token) {
    localStorage.setItem('authToken', token);
  } else {
    localStorage.removeItem('authToken');
  }
};

// Helper to get auth headers
const getAuthHeaders = (): HeadersInit => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }
  
  return headers;
};

// Helper to parse dates from API responses
const parseUser = (data: any): User => ({
  ...data,
  createdAt: new Date(data.createdAt),
});

const parseLeaderboardEntry = (data: any): LeaderboardEntry => ({
  ...data,
  timestamp: new Date(data.timestamp),
});

const parseGameSession = (data: any): GameSession => ({
  ...data,
  startedAt: new Date(data.startedAt),
  endedAt: data.endedAt ? new Date(data.endedAt) : undefined,
});

// Auth API
export const authApi = {
  async login(email: string, password: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      
      if (data.success && data.token) {
        setAuthToken(data.token);
      }
      
      return {
        ...data,
        user: data.user ? parseUser(data.user) : undefined,
      };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  },
  
  async signup(username: string, email: string, password: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });
      
      const data = await response.json();
      
      if (data.success && data.token) {
        setAuthToken(data.token);
      }
      
      return {
        ...data,
        user: data.user ? parseUser(data.user) : undefined,
      };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  },
  
  async logout(): Promise<{ success: boolean }> {
    try {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: getAuthHeaders(),
      });
      
      setAuthToken(null);
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      setAuthToken(null);
      return { success: true }; // Always succeed locally
    }
  },
  
  async getCurrentUser(): Promise<AuthResponse> {
    if (!authToken) {
      return { success: false, error: 'Not authenticated' };
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      
      const data = await response.json();
      
      if (!data.success || response.status === 401) {
        setAuthToken(null);
        return { success: false, error: 'Session expired' };
      }
      
      return {
        ...data,
        user: data.user ? parseUser(data.user) : undefined,
        token: authToken,
      };
    } catch (error) {
      console.error('Get current user error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  },
  
  async updateProfile(updates: Partial<User>): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/profile`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(updates),
      });
      
      const data = await response.json();
      
      return {
        ...data,
        user: data.user ? parseUser(data.user) : undefined,
      };
    } catch (error) {
      console.error('Update profile error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  },
};

// Leaderboard API
export const leaderboardApi = {
  async getLeaderboard(limit: number = 10): Promise<LeaderboardResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/leaderboard?limit=${limit}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      
      const data = await response.json();
      
      return {
        ...data,
        entries: data.entries ? data.entries.map(parseLeaderboardEntry) : [],
      };
    } catch (error) {
      console.error('Get leaderboard error:', error);
      return { success: false, entries: [], error: 'Network error. Please try again.' };
    }
  },
  
  async submitScore(score: number, chops: number): Promise<LeaderboardResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/leaderboard`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ score, chops }),
      });
      
      const data = await response.json();
      
      return {
        ...data,
        entries: data.entries ? data.entries.map(parseLeaderboardEntry) : [],
      };
    } catch (error) {
      console.error('Submit score error:', error);
      return { success: false, entries: [], error: 'Network error. Please try again.' };
    }
  },
};

// Game Session API
export const gameApi = {
  async startSession(): Promise<GameSessionResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/game/session`, {
        method: 'POST',
        headers: getAuthHeaders(),
      });
      
      const data = await response.json();
      
      return {
        ...data,
        session: data.session ? parseGameSession(data.session) : undefined,
      };
    } catch (error) {
      console.error('Start session error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  },
  
  async endSession(sessionId: string, score: number, chops: number, duration: number): Promise<GameSessionResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/game/session/${sessionId}/end`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ score, chops, duration }),
      });
      
      const data = await response.json();
      
      return {
        ...data,
        session: data.session ? parseGameSession(data.session) : undefined,
      };
    } catch (error) {
      console.error('End session error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  },
  
  async getStats(): Promise<{ success: boolean; stats?: { totalGames: number; avgScore: number; topScore: number }; error?: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/game/stats`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Get stats error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  },
};

// Export a combined API object for easy access
export const api = {
  auth: authApi,
  leaderboard: leaderboardApi,
  game: gameApi,
};

export default api;
