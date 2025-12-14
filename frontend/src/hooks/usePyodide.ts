import { useState, useEffect, useRef, useCallback } from 'react';
import { loadPyodide, type PyodideInterface } from 'pyodide';

interface UsePyodideReturn {
  runPython: (code: string) => Promise<string>;
  loading: boolean;
  error: string | null;
}

export function usePyodide(): UsePyodideReturn {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const pyodideRef = useRef<PyodideInterface | null>(null);

  // Load Pyodide once on mount
  useEffect(() => {
    let cancelled = false;

    async function initPyodide() {
      try {
        setLoading(true);
        setError(null);
        
        // Load Pyodide from CDN
        const pyodide = await loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/',
        });
        
        if (!cancelled) {
          pyodideRef.current = pyodide;
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to load Pyodide');
          setLoading(false);
        }
      }
    }

    initPyodide();

    return () => {
      cancelled = true;
    };
  }, []);

  const runPython = useCallback(async (code: string): Promise<string> => {
    if (!pyodideRef.current) {
      throw new Error('Pyodide is not loaded yet');
    }

    try {
      // Capture stdout
      const pyodide = pyodideRef.current;
      
      // Set up stdout capture
      await pyodide.runPythonAsync(`
import sys
import io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
      `);

      // Run the user's code
      await pyodide.runPythonAsync(code);

      // Get the output
      const stdout = await pyodide.runPythonAsync('sys.stdout.getvalue()');
      const stderr = await pyodide.runPythonAsync('sys.stderr.getvalue()');

      // Combine stdout and stderr
      let output = '';
      if (stdout) output += stdout;
      if (stderr) output += stderr;

      return output || 'Code executed successfully (no output)';
    } catch (err) {
      // Return the error message
      if (err instanceof Error) {
        return `Error: ${err.message}`;
      }
      return 'An unknown error occurred';
    }
  }, []);

  return { runPython, loading, error };
}
