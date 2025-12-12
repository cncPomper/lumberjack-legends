import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import React from 'react';

// Test component to access auth context
const TestComponent = () => {
  const { user, isAuthenticated, login, logout } = useAuth();
  
  return (
    <div>
      <div data-testid="auth-status">{isAuthenticated ? 'authenticated' : 'not-authenticated'}</div>
      <div data-testid="username">{user?.username || 'no-user'}</div>
      <button data-testid="login-btn" onClick={() => login('king@forest.com', 'password')}>Login</button>
      <button data-testid="logout-btn" onClick={logout}>Logout</button>
    </div>
  );
};

const renderWithProvider = () => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render auth provider without crashing', () => {
    const { getByTestId } = renderWithProvider();
    expect(getByTestId('auth-status')).toBeDefined();
  });

  it('should have login and logout buttons', () => {
    const { getByTestId } = renderWithProvider();
    expect(getByTestId('login-btn')).toBeDefined();
    expect(getByTestId('logout-btn')).toBeDefined();
  });
});
