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
      <h1 className="text-3xl font-bold mb-6">Code Syntax Highlighting</h1>
      
      <div className="space-y-8">
        <section>
          <h2 className="text-2xl font-semibold mb-4">JavaScript Example</h2>
          <CodeBlock 
            code={javascriptExample} 
            language="javascript"
          />
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Python Example</h2>
          <CodeBlock 
            code={pythonExample} 
            language="python"
          />
        </section>
      </div>
    </div>
  );
}
