import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { usePyodide } from './usePyodide';

// Mock Pyodide
vi.mock('pyodide', () => ({
  loadPyodide: vi.fn(() => Promise.resolve({
    runPythonAsync: vi.fn((code: string) => {
      if (code.includes('sys.stdout.getvalue()')) {
        return Promise.resolve('Test output\n');
      }
      if (code.includes('sys.stderr.getvalue()')) {
        return Promise.resolve('');
      }
      if (code.includes('raise Exception')) {
        return Promise.reject(new Error('Python exception'));
      }
      return Promise.resolve(undefined);
    }),
  })),
}));

describe('usePyodide', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize Pyodide on mount', async () => {
    const { result } = renderHook(() => usePyodide());

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBeNull();
  });

  it('should run Python code and return output', async () => {
    const { result } = renderHook(() => usePyodide());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const output = await result.current.runPython('print("Hello")');
    expect(output).toContain('Test output');
  });

  it('should handle Python errors gracefully', async () => {
    const { result } = renderHook(() => usePyodide());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const output = await result.current.runPython('raise Exception("test error")');
    expect(output).toContain('Error');
  });
});
