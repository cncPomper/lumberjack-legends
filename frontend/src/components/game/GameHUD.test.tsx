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
    const { getByText, getByTestId } = renderWithProviders();
    
    expect(getByText('Score')).toBeInTheDocument();
    expect(getByTestId('hud-score')).toHaveTextContent('0');
  });

  it('should render time display', () => {
    const { getByText, getByTestId } = renderWithProviders();
    
    expect(getByText('Time')).toBeInTheDocument();
    // Ensure the time element is present and contains "s"
    expect(getByTestId('hud-time').textContent).toContain('s');
  });

  it('should render chops display', () => {
    const { getByText, getByTestId } = renderWithProviders();
    
    expect(getByText('Chops')).toBeInTheDocument();
    expect(getByTestId('hud-chops')).toHaveTextContent('0');
  });
});