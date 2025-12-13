// Centralized Mock API Service for Lumberjack Game
// All backend calls are mocked here for easy future integration

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
}

export interface GameSessionResponse {
  success: boolean;
  session?: GameSession;
  error?: string;
}

// Simulated delay for realistic API behavior
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Original mock data (used for resetting)
const _initialMockUsers: User[] = [
  { id: '1', username: 'ForestKing', email: 'king@forest.com', createdAt: new Date('2024-01-15'), highScore: 2500, totalChops: 15000, gamesPlayed: 120 },
  { id: '2', username: 'AxeMaster', email: 'axe@master.com', createdAt: new Date('2024-02-20'), highScore: 2200, totalChops: 12000, gamesPlayed: 95 },
  { id: '3', username: 'TimberWolf', email: 'timber@wolf.com', createdAt: new Date('2024-03-10'), highScore: 1950, totalChops: 9500, gamesPlayed: 78 },
  { id: '4', username: 'WoodChuck', email: 'wood@chuck.com', createdAt: new Date('2024-04-05'), highScore: 1800, totalChops: 8200, gamesPlayed: 65 },
  { id: '5', username: 'TreeHugger', email: 'tree@hugger.com', createdAt: new Date('2024-05-12'), highScore: 1650, totalChops: 7100, gamesPlayed: 52 },
  { id: '6', username: 'LogLegend', email: 'log@legend.com', createdAt: new Date('2024-06-08'), highScore: 1500, totalChops: 6000, gamesPlayed: 45 },
  { id: '7', username: 'ChopChamp', email: 'chop@champ.com', createdAt: new Date('2024-07-22'), highScore: 1350, totalChops: 5200, gamesPlayed: 38 },
  { id: '8', username: 'SawdustSam', email: 'saw@dust.com', createdAt: new Date('2024-08-15'), highScore: 1200, totalChops: 4500, gamesPlayed: 32 },
  { id: '9', username: 'BarkBuster', email: 'bark@buster.com', createdAt: new Date('2024-09-01'), highScore: 1050, totalChops: 3800, gamesPlayed: 28 },
  { id: '10', username: 'Timberton', email: 'timber@ton.com', createdAt: new Date('2024-10-10'), highScore: 900, totalChops: 3200, gamesPlayed: 22 },
];

// Mock data storage (simulates database) - these will be reset by the function below
export let mockUsers: User[] = JSON.parse(JSON.stringify(_initialMockUsers)); // Deep copy
export let currentUser: User | null = null;
export let authToken: string | null = null;

// Function to reset the internal state of the mock API for tests
export const __resetMockApiState = () => {
  mockUsers = JSON.parse(JSON.stringify(_initialMockUsers));
  currentUser = null;
  authToken = null;
};

// Generate mock token
const generateToken = () => Math.random().toString(36).substring(2) + Date.now().toString(36);

// Auth API
export const mockAuthApi = {
  async login(email: string, password: string): Promise<AuthResponse> {
    await delay(800);
    
    // Simulate validation
    if (!email || !password) {
      return { success: false, error: 'Email and password are required' };
    }
    
    const user = mockUsers.find(u => u.email.toLowerCase() === email.toLowerCase());
    
    if (!user) {
      return { success: false, error: 'Invalid email or password' };
    }
    
    // In real app, we'd verify password hash
    if (password.length < 4) { // Simplified for mock
      return { success: false, error: 'Invalid email or password' };
    }
    
    currentUser = user;
    authToken = generateToken();
    
    return { success: true, user, token: authToken };
  },
  
  async signup(username: string, email: string, password: string): Promise<AuthResponse> {
    await delay(1000);
    
    // Validation
    if (!username || username.length < 3) {
      return { success: false, error: 'Username must be at least 3 characters' };
    }
    
    if (!email || !email.includes('@')) {
      return { success: false, error: 'Please enter a valid email' };
    }
    
    if (!password || password.length < 6) {
      return { success: false, error: 'Password must be at least 6 characters' };
    }
    
    // Check if email exists
    if (mockUsers.some(u => u.email.toLowerCase() === email.toLowerCase())) {
      return { success: false, error: 'Email already registered' };
    }
    
    // Check if username exists
    if (mockUsers.some(u => u.username.toLowerCase() === username.toLowerCase())) {
      return { success: false, error: 'Username already taken' };
    }
    
    const newUser: User = {
      id: (mockUsers.length + 1).toString(),
      username,
      email,
      createdAt: new Date(),
      highScore: 0,
      totalChops: 0,
      gamesPlayed: 0,
    };
    
    mockUsers.push(newUser);
    currentUser = newUser;
    authToken = generateToken();
    
    return { success: true, user: newUser, token: authToken };
  },
  
  async logout(): Promise<{ success: boolean }> {
    await delay(300);
    currentUser = null;
    authToken = null;
    return { success: true };
  },
  
  async getCurrentUser(): Promise<AuthResponse> {
    await delay(200);
    
    if (!currentUser || !authToken) {
      return { success: false, error: 'Not authenticated' };
    }
    
    return { success: true, user: currentUser, token: authToken };
  },
  
  async updateProfile(updates: Partial<User>): Promise<AuthResponse> {
    await delay(500);
    
    if (!currentUser) {
      return { success: false, error: 'Not authenticated' };
    }
    
    currentUser = { ...currentUser, ...updates };
    const userIndex = mockUsers.findIndex(u => u.id === currentUser!.id);
    if (userIndex !== -1) {
      mockUsers[userIndex] = currentUser;
    }
    
    return { success: true, user: currentUser };
  },
};

// Leaderboard API
export const mockLeaderboardApi = {
  async getLeaderboard(limit: number = 10): Promise<LeaderboardResponse> {
    await delay(600);
    
    const sortedUsers = [...mockUsers]
      .sort((a, b) => b.highScore - a.highScore)
      .slice(0, limit);
    
    const entries: LeaderboardEntry[] = sortedUsers.map((user, index) => ({
      id: user.id,
      username: user.username,
      score: user.highScore,
      chops: user.totalChops,
      rank: index + 1,
      timestamp: new Date(),
    }));
    
    let userRank: number | undefined;
    if (currentUser) {
      const allSorted = [...mockUsers].sort((a, b) => b.highScore - a.highScore);
      userRank = allSorted.findIndex(u => u.id === currentUser!.id) + 1;
    }
    
    return { success: true, entries, userRank };
  },
  
  async submitScore(score: number, chops: number): Promise<LeaderboardResponse> {
    await delay(700);
    
    if (!currentUser) {
      return { success: false, entries: [] };
    }
    
    // Update user stats
    if (score > currentUser.highScore) {
      currentUser.highScore = score;
    }
    currentUser.totalChops += chops;
    currentUser.gamesPlayed += 1;
    
    const userIndex = mockUsers.findIndex(u => u.id === currentUser!.id);
    if (userIndex !== -1) {
      mockUsers[userIndex] = currentUser;
    }
    
    return this.getLeaderboard();
  },
};

// Game Session API
export const mockGameApi = {
  async startSession(): Promise<GameSessionResponse> {
    await delay(300);
    
    const session: GameSession = {
      id: generateToken(),
      userId: currentUser?.id || 'guest',
      score: 0,
      chops: 0,
      duration: 0,
      startedAt: new Date(),
    };
    
    return { success: true, session };
  },
  
  async endSession(sessionId: string, score: number, chops: number, duration: number): Promise<GameSessionResponse> {
    await delay(400);
    
    const session: GameSession = {
      id: sessionId,
      userId: currentUser?.id || 'guest',
      score,
      chops,
      duration,
      startedAt: new Date(Date.now() - duration * 1000),
      endedAt: new Date(),
    };
    
    // Update leaderboard if logged in
    if (currentUser) {
      await mockLeaderboardApi.submitScore(score, chops);
    }
    
    return { success: true, session };
  },
  
  async getStats(): Promise<{ success: boolean; stats?: { totalGames: number; avgScore: number; topScore: number } }> {
    await delay(400);
    
    if (!currentUser) {
      return { success: false };
    }
    
    return {
      success: true,
      stats: {
        totalGames: currentUser.gamesPlayed,
        avgScore: currentUser.gamesPlayed > 0 ? Math.round(currentUser.totalChops / currentUser.gamesPlayed) : 0,
        topScore: currentUser.highScore,
      },
    };
  },
};

// Export a combined API object for easy access
export const api = {
  auth: mockAuthApi,
  leaderboard: mockLeaderboardApi,
  game: mockGameApi,
  __resetMockApiState, // Export the reset function
};

export default api;