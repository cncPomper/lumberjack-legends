import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '@/contexts/AuthContext';
import { GameProvider } from '@/contexts/GameContext';
import GameHUD from './GameHUD';
import React from 'react';

const renderWithProviders = () => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <GameProvider>
          <GameHUD />
        </GameProvider>
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('GameHUD', () => {
  it('should render score display', () => {
    const { getByText } = renderWithProviders();
    
    expect(getByText('Score')).toBeInTheDocument();
    expect(getByText('0')).toBeInTheDocument();
  });

  it('should render time display', () => {
    const { getByText } = renderWithProviders();
    
    expect(getByText('Time')).toBeInTheDocument();
  });

  it('should render chops display', () => {
    const { getByText } = renderWithProviders();
    
    expect(getByText('Chops')).toBeInTheDocument();
  });
});
