import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '@/contexts/AuthContext';
import { GameProvider } from '@/contexts/GameContext';
import GameOverlay from './GameOverlay';
import React from 'react';

const renderWithProviders = () => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <GameProvider>
          <GameOverlay />
        </GameProvider>
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('GameOverlay', () => {
  it('should show start screen when game is idle', () => {
    const { getByText } = renderWithProviders();
    
    expect(getByText('🪓 Lumberjack')).toBeInTheDocument();
    expect(getByText('Start Game')).toBeInTheDocument();
  });

  it('should show controls instructions', () => {
    const { getByText } = renderWithProviders();
    
    expect(getByText('Controls')).toBeInTheDocument();
  });

  it('should have sign in prompt for non-authenticated users', () => {
    const { getByText } = renderWithProviders();
    
    expect(getByText(/Sign in/)).toBeInTheDocument();
  });
});
