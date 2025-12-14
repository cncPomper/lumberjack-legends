import { CodeBlock } from '@/components/ui/code-block';

const javascriptExample = `// JavaScript Example
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(10);
console.log(\`Fibonacci(10) = \${result}\`);`;

const pythonExample = `# Python Example
def factorial(n):
    """Calculate factorial using recursion"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"Factorial(5) = {result}")`;

export function CodeExamplesPage() {
  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Code Examples</h1>
      
      <div className="mb-6 p-4 bg-blue-950 border border-blue-800 rounded-lg text-blue-200 text-sm">
        <strong>✨ Python code is now executable!</strong> Click the "Run" button to execute Python code directly in your browser using WebAssembly (Pyodide).
      </div>
      
      <div className="space-y-8">
        <section>
          <h2 className="text-2xl font-semibold mb-4">JavaScript Example</h2>
          <p className="text-sm text-muted-foreground mb-3">
            Syntax highlighting only (JavaScript execution requires eval, which is disabled for security)
          </p>
          <CodeBlock 
            code={javascriptExample} 
            language="javascript"
          />
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Python Example (Executable)</h2>
          <p className="text-sm text-muted-foreground mb-3">
            This Python code runs in your browser using Pyodide (Python compiled to WebAssembly)
          </p>
          <CodeBlock 
            code={pythonExample} 
            language="python"
            executable
          />
        </section>
      </div>
    </div>
  );
}
