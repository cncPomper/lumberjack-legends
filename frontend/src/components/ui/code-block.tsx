import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from './button';
import { Play, Loader2 } from 'lucide-react';
import { usePyodide } from '@/hooks/usePyodide';

interface CodeBlockProps {
  code: string;
  language: 'javascript' | 'python' | 'typescript' | 'jsx' | 'tsx';
  showLineNumbers?: boolean;
  className?: string;
  executable?: boolean;
}

export function CodeBlock({ 
  code, 
  language, 
  showLineNumbers = true,
  className = '',
  executable = false
}: CodeBlockProps) {
  const [output, setOutput] = useState<string>('');
  const [isRunning, setIsRunning] = useState(false);
  const { runPython, loading: pyodideLoading, error: pyodideError } = usePyodide();

  const canExecute = executable && language === 'python';

  const handleRun = async () => {
    if (!canExecute) return;
    
    setIsRunning(true);
    setOutput('');
    
    try {
      const result = await runPython(code);
      setOutput(result);
    } catch (err) {
      setOutput(err instanceof Error ? err.message : 'Execution failed');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className={`rounded-lg overflow-hidden ${className}`}>
      <div className="relative">
        {canExecute && (
          <div className="absolute top-2 right-2 z-10">
            <Button
              size="sm"
              variant="secondary"
              onClick={handleRun}
              disabled={isRunning || pyodideLoading}
              className="gap-2"
            >
              {isRunning ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Running...
                </>
              ) : pyodideLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Loading...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  Run
                </>
              )}
            </Button>
          </div>
        )}
        
        <SyntaxHighlighter
          language={language}
          style={vscDarkPlus}
          showLineNumbers={showLineNumbers}
          customStyle={{
            margin: 0,
            borderRadius: '0.5rem',
            fontSize: '0.875rem',
            paddingTop: canExecute ? '3rem' : '1rem',
          }}
          lineNumberStyle={{
            minWidth: '3em',
            paddingRight: '1em',
            color: '#6e7681',
            userSelect: 'none',
          }}
        >
          {code}
        </SyntaxHighlighter>
      </div>

      {canExecute && pyodideError && (
        <div className="mt-2 p-3 bg-red-950 border border-red-800 rounded-lg text-red-200 text-sm">
          <strong>Pyodide Error:</strong> {pyodideError}
        </div>
      )}

      {canExecute && output && (
        <div className="mt-2 p-4 bg-zinc-900 border border-zinc-700 rounded-lg">
          <div className="text-xs text-zinc-400 mb-2 font-semibold">Output:</div>
          <pre className="text-sm text-zinc-100 whitespace-pre-wrap font-mono">
            {output}
          </pre>
        </div>
      )}
    </div>
  );
}
