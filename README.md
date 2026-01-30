# AnyDef

A Python library that uses AI to auto-generate function implementations based on their signatures and docstrings. Generated code runs safely in an isolated sandbox environment.

## Features

- **AI-Powered**: Uses OpenAI models to generate function implementations
- **Secure Sandbox**: Code executes in [PyodideSandbox](https://github.com/langchain-ai/langchain-sandbox) (WebAssembly-based isolation)
- **Simple API**: Just add a decorator and docstring
- **Async Support**: Both sync and async decorators available
- **Caching**: Generated code is cached per function

## Installation

```bash
pip install anydef
```

### Prerequisites

**Deno** is required for the sandbox environment:

```bash
# macOS
brew install deno

# Linux
curl -fsSL https://deno.land/install.sh | sh

# Windows
irm https://deno.land/install.ps1 | iex
```

## Quick Start

Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Use the `@anydef` decorator:

```python
from anydef import anydef

@anydef
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    pass

result = fibonacci(10)
print(result)  # Output: 55
```

## Usage

### Basic Usage

```python
from anydef import anydef

@anydef
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    pass

print(is_prime(17))  # True
print(is_prime(4))   # False
```

### Specifying a Model

```python
@anydef(model="gpt-4")
def complex_algorithm(data: list) -> list:
    """Sort the list using merge sort algorithm."""
    pass
```

### Debug Mode

```python
@anydef(debug=True)
def factorial(n: int) -> int:
    """Calculate the factorial of n."""
    pass

# This will print the generated code before execution
factorial(5)
```

### Custom Timeout

```python
@anydef(timeout=60)  # 60 seconds timeout
def slow_computation(n: int) -> int:
    """Perform a computation that might take a while."""
    pass
```

### Async Functions

```python
from anydef import anydef_async
import asyncio

@anydef_async
async def async_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    pass

async def main():
    result = await async_fibonacci(10)
    print(result)  # 55

asyncio.run(main())
```

## How It Works

1. **Decorator captures** the function signature and docstring
2. **AI generates** the implementation based on the description
3. **Code executes** in an isolated PyodideSandbox (WebAssembly)
4. **Result returns** to your Python program

```
┌─────────────┐    ┌─────────────┐    ┌─────────────────┐    ┌────────┐
│  @anydef    │───▶│  OpenAI API │───▶│ PyodideSandbox  │───▶│ Result │
│  decorator  │    │  (generate) │    │ (safe execute)  │    │        │
└─────────────┘    └─────────────┘    └─────────────────┘    └────────┘
```

## Security

Generated code runs in **PyodideSandbox**, which provides:

- **WebAssembly isolation**: Code runs in a Pyodide environment (Python compiled to WASM)
- **No filesystem access**: Cannot read/write files on your system
- **No network access**: Cannot make HTTP requests (configurable)
- **Resource limits**: Timeout protection against infinite loops

## API Reference

### `@anydef`

```python
@anydef(
    model: str = "gpt-3.5-turbo",  # OpenAI model to use
    timeout: int = 30,             # Execution timeout in seconds
    debug: bool = False            # Print generated code
)
```

### `@anydef_async`

Same parameters as `@anydef`, but for async functions.

## Requirements

- Python 3.8+
- Deno runtime
- OpenAI API key

## Limitations

- Generated code must be self-contained (standard library only inside sandbox)
- Results must be JSON-serializable (primitives, lists, dicts)
- First call has latency due to sandbox initialization (~2-3 seconds)
- Subsequent calls are faster due to code caching

## License

MIT License - see [LICENSE](LICENSE) for details.
