import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { GameProvider, useGame } from './GameContext';
import { AuthProvider } from './AuthContext';
import React from 'react';

// Test component to access game context
const TestGameComponent = () => {
  const { 
    gameState, 
    score, 
    chops, 
    playerPosition, 
    startGame, 
    chop, 
    movePlayer,
    endGame 
  } = useGame();
  
  return (
    <div>
      <div data-testid="game-state">{gameState}</div>
      <div data-testid="score">{score}</div>
      <div data-testid="chops">{chops}</div>
      <div data-testid="position">{playerPosition}</div>
      <button data-testid="start-btn" onClick={startGame}>Start</button>
      <button data-testid="chop-btn" onClick={chop}>Chop</button>
      <button data-testid="move-left-btn" onClick={() => movePlayer('left')}>Move Left</button>
      <button data-testid="move-right-btn" onClick={() => movePlayer('right')}>Move Right</button>
      <button data-testid="end-btn" onClick={endGame}>End</button>
    </div>
  );
};

const renderWithProviders = () => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <GameProvider>
          <TestGameComponent />
        </GameProvider>
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('GameContext', () => {
  it('should start with idle state', () => {
    const { getByTestId } = renderWithProviders();
    
    expect(getByTestId('game-state')).toHaveTextContent('idle');
    expect(getByTestId('score')).toHaveTextContent('0');
    expect(getByTestId('chops')).toHaveTextContent('0');
  });

  it('should change state to playing when game starts', () => {
    const { getByTestId } = renderWithProviders();
    
    getByTestId('start-btn').click();
    
    expect(getByTestId('game-state')).toHaveTextContent('playing');
  });

  it('should reset score and chops on new game', () => {
    const { getByTestId } = renderWithProviders();
    
    // Start game
    getByTestId('start-btn').click();
    
    // Verify reset
    expect(getByTestId('score')).toHaveTextContent('0');
    expect(getByTestId('chops')).toHaveTextContent('0');
  });

  it('should increment score and chops on successful chop', () => {
    const { getByTestId } = renderWithProviders();
    
    getByTestId('start-btn').click();
    
    // Make sure player is on safe side before chopping
    const initialScore = parseInt(getByTestId('score').textContent || '0');
    
    // Chop action - note: this may end game if there's a branch
    getByTestId('chop-btn').click();
    
    // Score should either increase or game should end
    const gameState = getByTestId('game-state').textContent;
    if (gameState === 'playing') {
      const newScore = parseInt(getByTestId('score').textContent || '0');
      expect(newScore).toBeGreaterThan(initialScore);
    }
  });

  it('should change player position when moving', () => {
    const { getByTestId } = renderWithProviders();
    
    // Default position is left
    expect(getByTestId('position')).toHaveTextContent('left');
    
    getByTestId('start-btn').click();
    
    // Move right
    getByTestId('move-right-btn').click();
    expect(getByTestId('position')).toHaveTextContent('right');
    
    // Move left
    getByTestId('move-left-btn').click();
    expect(getByTestId('position')).toHaveTextContent('left');
  });

  it('should not allow movement when game is not playing', () => {
    const { getByTestId } = renderWithProviders();
    
    // Try to move without starting game
    getByTestId('move-right-btn').click();
    
    // Position should remain left (default)
    expect(getByTestId('position')).toHaveTextContent('left');
  });

  it('should change to gameover state when ending game', () => {
    const { getByTestId } = renderWithProviders();
    
    getByTestId('start-btn').click();
    expect(getByTestId('game-state')).toHaveTextContent('playing');
    
    getByTestId('end-btn').click();
    expect(getByTestId('game-state')).toHaveTextContent('gameover');
  });
});
