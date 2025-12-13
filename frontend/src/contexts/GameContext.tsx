import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { api } from '@/services/api';
import { useAuth } from './AuthContext';

export type GameState = 'idle' | 'playing' | 'paused' | 'gameover';
export type PlayerPosition = 'left' | 'right';
export type BranchSide = 'left' | 'right' | 'none';

export interface TreeSegment {
  id: number;
  branch: BranchSide;
}

interface GameContextType {
  gameState: GameState;
  score: number;
  chops: number;
  timeLeft: number;
  playerPosition: PlayerPosition;
  treeSegments: TreeSegment[];
  isChopping: boolean;
  startGame: () => void;
  pauseGame: () => void;
  resumeGame: () => void;
  endGame: () => void;
  chop: () => void;
  movePlayer: (position: PlayerPosition) => void;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

const INITIAL_TIME = 10; // seconds
const TIME_BONUS = 0.5; // seconds added per chop
const TREE_HEIGHT = 6; // number of segments visible

// Generate random tree segment
const generateSegment = (id: number): TreeSegment => {
  const random = Math.random();
  let branch: BranchSide = 'none';
  
  if (random < 0.35) branch = 'left';
  else if (random < 0.7) branch = 'right';
  
  return { id, branch };
};

// Generate initial tree
const generateTree = (): TreeSegment[] => {
  return Array.from({ length: TREE_HEIGHT }, (_, i) => generateSegment(i));
};

export function GameProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [gameState, setGameState] = useState<GameState>('idle');
  const [score, setScore] = useState(0);
  const [chops, setChops] = useState(0);
  const [timeLeft, setTimeLeft] = useState(INITIAL_TIME);
  const [playerPosition, setPlayerPosition] = useState<PlayerPosition>('left');
  const [treeSegments, setTreeSegments] = useState<TreeSegment[]>(generateTree);
  const [isChopping, setIsChopping] = useState(false);
  const [timerRef, setTimerRef] = useState<NodeJS.Timeout | null>(null);
  const [segmentCounter, setSegmentCounter] = useState(TREE_HEIGHT);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [gameStartTime, setGameStartTime] = useState<number>(0);

  const endGame = useCallback(async () => {
    if (timerRef) {
      clearInterval(timerRef);
      setTimerRef(null);
    }
    setGameState('gameover');
    
    // Submit score and end session if user is logged in
    if (user && sessionId) {
      const duration = (Date.now() - gameStartTime) / 1000; // Convert to seconds
      await api.game.endSession(sessionId, score, chops, duration);
    }
  }, [timerRef, user, sessionId, score, chops, gameStartTime]);

  const startGame = useCallback(async () => {
    setScore(0);
    setChops(0);
    setTimeLeft(INITIAL_TIME);
    setPlayerPosition('left');
    setTreeSegments(generateTree());
    setSegmentCounter(TREE_HEIGHT);
    setGameState('playing');
    setGameStartTime(Date.now());

    // Start a game session if user is logged in
    if (user) {
      const sessionResponse = await api.game.startSession();
      if (sessionResponse.success && sessionResponse.session) {
        setSessionId(sessionResponse.session.id);
      }
    }

    // Start timer
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 0.1) {
          return 0;
        }
        return Math.max(0, prev - 0.1);
      });
    }, 100);
    
    setTimerRef(timer);
  }, [user]);

  // Check for game over when time runs out
  React.useEffect(() => {
    if (gameState === 'playing' && timeLeft <= 0) {
      endGame();
    }
  }, [timeLeft, gameState, endGame]);

  const pauseGame = useCallback(() => {
    if (timerRef) {
      clearInterval(timerRef);
      setTimerRef(null);
    }
    setGameState('paused');
  }, [timerRef]);

  const resumeGame = useCallback(() => {
    setGameState('playing');
    const timer = setInterval(() => {
      setTimeLeft(prev => Math.max(0, prev - 0.1));
    }, 100);
    setTimerRef(timer);
  }, []);

  const chop = useCallback(() => {
    if (gameState !== 'playing' || isChopping) return;

    // Check if player will be hit by branch
    const bottomSegment = treeSegments[0];
    if (bottomSegment.branch === playerPosition) {
      endGame();
      return;
    }

    // Perform chop
    setIsChopping(true);
    setChops(prev => prev + 1);
    setScore(prev => prev + 10);
    setTimeLeft(prev => Math.min(INITIAL_TIME, prev + TIME_BONUS));

    // Move tree down
    setTreeSegments(prev => {
      const newTree = prev.slice(1);
      setSegmentCounter(c => {
        const newSegment = generateSegment(c);
        newTree.push(newSegment);
        return c + 1;
      });
      return newTree;
    });

    // Reset chopping animation
    setTimeout(() => {
      setIsChopping(false);
    }, 100);
  }, [gameState, isChopping, treeSegments, playerPosition, endGame]);

  const movePlayer = useCallback((position: PlayerPosition) => {
    if (gameState !== 'playing') return;
    setPlayerPosition(position);
  }, [gameState]);

  // Cleanup timer on unmount
  React.useEffect(() => {
    return () => {
      if (timerRef) {
        clearInterval(timerRef);
      }
    };
  }, [timerRef]);

  return (
    <GameContext.Provider
      value={{
        gameState,
        score,
        chops,
        timeLeft,
        playerPosition,
        treeSegments,
        isChopping,
        startGame,
        pauseGame,
        resumeGame,
        endGame,
        chop,
        movePlayer,
      }}
    >
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  const context = useContext(GameContext);
  if (context === undefined) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
}
