# AnyDef Development Guide

## Project Overview

AnyDef is a Python library that uses AI to auto-generate function implementations based on their signatures and docstrings. Generated code executes safely in an isolated PyodideSandbox environment (WebAssembly-based).

## Project Structure

```
anydef/
├── anydef/                 # Main package
│   ├── __init__.py         # Package exports (anydef, anydef_async)
│   ├── core.py             # Core decorator implementation
│   ├── version.py          # Version information
│   └── __main__.py         # CLI entry point
├── tests/                  # Test suite
│   └── test_anydef.py      # Unit tests (sync & async)
├── examples/               # Usage examples
├── docs/                   # Documentation
├── setup.py                # Package setup
├── pyproject.toml          # Project configuration
├── requirements.txt        # Production dependencies
└── requirements-dev.txt    # Development dependencies
```

## Quick Start

### 1. Install Prerequisites

**Deno** is required for the sandbox:

```bash
# macOS
brew install deno

# Linux
curl -fsSL https://deno.land/install.sh | sh
```

### 2. Clone and Setup

```bash
git clone https://github.com/yourusername/anydef.git
cd anydef

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt
```

### 3. Configure API Key

```bash
export OPENAI_API_KEY=your_api_key_here
```

### 4. Run Tests

```bash
pytest tests/ -v
```

## Core Architecture

### Flow Diagram

```
┌──────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────┐
│  @anydef     │───▶│  OpenAI API  │───▶│ PyodideSandbox  │───▶│ Result │
│  decorator   │    │  (generate)  │    │ (WASM execute)  │    │        │
└──────────────┘    └──────────────┘    └─────────────────┘    └────────┘
```

### Key Components

1. **`_generate_code()`**: Calls OpenAI API to generate function implementation
2. **`_execute_in_sandbox()`**: Runs code in PyodideSandbox (async)
3. **`anydef`**: Sync decorator (uses `asyncio.run()` internally)
4. **`anydef_async`**: Async decorator for native async usage

### Decorator Parameters

```python
@anydef(
    model="gpt-3.5-turbo",  # OpenAI model
    timeout=30,              # Sandbox timeout (seconds)
    debug=False              # Print generated code
)
```

### Security: PyodideSandbox

Generated code runs in **PyodideSandbox** (LangChain), which provides:

- **WebAssembly Isolation**: Python runs in Pyodide (WASM), completely isolated
- **No Filesystem Access**: Cannot read/write host files
- **No Network Access**: Disabled by default (`allow_net=False`)
- **Timeout Protection**: Prevents infinite loops
- **Powered by Deno**: Secure runtime with fine-grained permissions

## Development Workflow

### Code Style

```bash
# Format
black .

# Lint
flake8

# Both before commit
black . && flake8
```

### Running Tests

```bash
# All tests
pytest

# Verbose
pytest -v

# Specific test class
pytest tests/test_anydef.py::TestAnydefSync

# Async tests only
pytest tests/test_anydef.py::TestAnydefAsync

# With different model
ANYDEF_TEST_MODEL=gpt-4 pytest
```

### Adding New Features

1. Create a feature branch
2. Write tests first (TDD)
3. Implement in `anydef/core.py`
4. Update `__init__.py` exports if needed
5. Update documentation

## Key Implementation Details

### Argument Serialization

Arguments are serialized to JSON to pass into the sandbox:

```python
# In _execute_in_sandbox()
execution_code = f'''
{generated_code}

import json
_args = json.loads({repr(args)})
_kwargs = json.loads({repr(kwargs)})
_result = {func_name}(*_args, **_kwargs)
print(json.dumps({{"__anydef_result__": _result}}))
'''
```

### Code Caching

Generated code is cached per function to avoid redundant API calls:

```python
_generated_code_cache: dict = {}

if func.__name__ not in _generated_code_cache:
    code = _generate_code(func, model)
    _generated_code_cache[func.__name__] = code
```

### Async Context Handling

The sync decorator handles both sync and async contexts:

```python
try:
    loop = asyncio.get_running_loop()
    # In async context: use ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(asyncio.run, coro)
        return future.result()
except RuntimeError:
    # Not in async context: use asyncio.run directly
    return asyncio.run(coro)
```

## Dependencies

### Production
- `openai>=1.0.0` - OpenAI API client
- `langchain-sandbox>=0.0.6` - PyodideSandbox

### Development
- `pytest>=6.0.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `black>=22.0.0` - Code formatter
- `flake8>=4.0.0` - Linter

## Debugging

### Enable Debug Mode

```python
@anydef(debug=True)
def my_function(...):
    ...
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Model not found` | Invalid model name | Check OpenAI docs for available models |
| `Sandbox timeout` | Code takes too long | Increase `timeout` parameter |
| `JSON decode error` | Non-serializable result | Ensure result is JSON-serializable |
| `Deno not found` | Deno not installed | Install Deno runtime |

## Release Process

1. Update version in `anydef/version.py`
2. Update `CHANGELOG.md`
3. Run full test suite: `pytest`
4. Create git tag: `git tag v0.x.x`
5. Build: `python -m build`
6. Upload: `twine upload dist/*`

## Roadmap

- [x] PyodideSandbox integration
- [x] Async support (`anydef_async`)
- [x] Code caching
- [ ] Multiple AI providers (Anthropic, etc.)
- [ ] Persistent code cache (file-based)
- [ ] Custom sandbox configurations
