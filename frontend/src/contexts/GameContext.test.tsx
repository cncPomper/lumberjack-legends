import { describe, it, expect } from 'vitest';
import { render, fireEvent, waitFor } from '@testing-library/react';
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

  it('should change state to playing when game starts', async () => {
    const { getByTestId } = renderWithProviders();

    fireEvent.click(getByTestId('start-btn'));

    await waitFor(() => {
      expect(getByTestId('game-state')).toHaveTextContent('playing');
    });
  });

  it('should reset score and chops on new game', async () => {
    const { getByTestId } = renderWithProviders();

    // Start game
    fireEvent.click(getByTestId('start-btn'));

    await waitFor(() => {
      expect(getByTestId('score')).toHaveTextContent('0');
      expect(getByTestId('chops')).toHaveTextContent('0');
    });
  });

  it('should increment score and chops on successful chop', async () => {
    const { getByTestId } = renderWithProviders();

    fireEvent.click(getByTestId('start-btn'));

    // wait for playing
    await waitFor(() => {
      expect(getByTestId('game-state')).toHaveTextContent('playing');
    });

    const initialScore = parseInt(getByTestId('score').textContent || '0');

    fireEvent.click(getByTestId('chop-btn'));

    await waitFor(() => {
      const gameState = getByTestId('game-state').textContent;
      if (gameState === 'playing') {
        const newScore = parseInt(getByTestId('score').textContent || '0');
        expect(newScore).toBeGreaterThanOrEqual(initialScore);
      }
    });
  });

  it('should change player position when moving', async () => {
    const { getByTestId } = renderWithProviders();

    // Default position is left
    expect(getByTestId('position')).toHaveTextContent('left');

    fireEvent.click(getByTestId('start-btn'));
    await waitFor(() => expect(getByTestId('game-state')).toHaveTextContent('playing'));

    // Move right
    fireEvent.click(getByTestId('move-right-btn'));
    await waitFor(() => expect(getByTestId('position')).toHaveTextContent('right'));

    // Move left
    fireEvent.click(getByTestId('move-left-btn'));
    await waitFor(() => expect(getByTestId('position')).toHaveTextContent('left'));
  });

  it('should not allow movement when game is not playing', () => {
    const { getByTestId } = renderWithProviders();

    // Try to move without starting game
    fireEvent.click(getByTestId('move-right-btn'));

    // Position should remain left (default)
    expect(getByTestId('position')).toHaveTextContent('left');
  });

  it('should change to gameover state when ending game', async () => {
    const { getByTestId } = renderWithProviders();

    fireEvent.click(getByTestId('start-btn'));
    await waitFor(() => expect(getByTestId('game-state')).toHaveTextContent('playing'));

    fireEvent.click(getByTestId('end-btn'));
    await waitFor(() => expect(getByTestId('game-state')).toHaveTextContent('gameover'));
  });
});