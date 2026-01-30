# Claude Code Instructions for AnyDef

This document provides guidance for Claude Code when assisting with the AnyDef project.

## Project Context

AnyDef is a Python library that uses AI to auto-generate function implementations. Users write function signatures with docstrings, and the `@anydef` decorator generates the implementation at runtime using OpenAI's API. Generated code executes safely in **PyodideSandbox** (WebAssembly isolation).

### Core Usage Pattern

```python
from anydef import anydef, anydef_async

# Sync version
@anydef
def function_name(param: Type) -> ReturnType:
    """Docstring describing what the function should do."""
    pass

result = function_name(arg)

# Async version
@anydef_async
async def async_function(param: Type) -> ReturnType:
    """Docstring describing behavior."""
    pass

result = await async_function(arg)
```

## Key Files

| File | Purpose |
|------|---------|
| `anydef/core.py` | Main implementation: `anydef`, `anydef_async`, `_generate_code()`, `_execute_in_sandbox()` |
| `anydef/__init__.py` | Package exports |
| `anydef/version.py` | Version string |
| `tests/test_anydef.py` | Test suite (sync & async) |
| `requirements.txt` | Runtime deps: `openai`, `langchain-sandbox` |

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────┐
│  @anydef     │───▶│  OpenAI API  │───▶│ PyodideSandbox  │───▶│ Result │
│  decorator   │    │  (generate)  │    │ (WASM execute)  │    │        │
└──────────────┘    └──────────────┘    └─────────────────┘    └────────┘
```

### Key Functions

1. **`_generate_code(func, model)`**: Calls OpenAI to generate Python code
2. **`_execute_in_sandbox(code, func_name, args, kwargs, timeout)`**: Runs code in PyodideSandbox
3. **`anydef`**: Sync decorator, wraps async execution with `asyncio.run()`
4. **`anydef_async`**: Native async decorator

## Code Conventions

### Style
- Black formatter (line length 88)
- PEP 8 compliance
- Type hints required for public functions
- Docstrings required for public functions

### Imports Order
1. Standard library (`asyncio`, `functools`, `inspect`)
2. Third-party (`openai`, `langchain_sandbox`)
3. Local imports

## Common Tasks

### Adding a New Decorator Parameter

1. Add parameter to both `anydef()` and `anydef_async()` signatures
2. Pass through in the nested `decorator()` function
3. Use in `_generate_code()` or `_execute_in_sandbox()` as needed
4. Add tests
5. Update README.md

Example:
```python
def anydef(
    func: Optional[Callable] = None,
    model: str = DEFAULT_MODEL,
    timeout: int = DEFAULT_TIMEOUT,
    debug: bool = False,
    new_param: str = "default",  # Add here
) -> Callable:
    if func is None:
        def decorator(f):
            return anydef(f, model=model, timeout=timeout, debug=debug, new_param=new_param)
        return decorator
    # ... use new_param
```

### Adding a New AI Provider

1. Create abstraction for code generation (e.g., `_generate_code_openai()`, `_generate_code_anthropic()`)
2. Add `provider` parameter to decorators
3. Update requirements.txt
4. Add provider-specific tests

### Modifying Sandbox Behavior

Edit `_execute_in_sandbox()` in `core.py`:

```python
sandbox = PyodideSandbox(
    allow_net=False,      # Network access
    timeout=timeout,      # Execution timeout
    # Add new options here
)
```

## Testing Requirements

### Before Any Commit
```bash
black .
flake8
pytest -v
```

### Test Pattern
```python
class TestFeature:
    def test_sync_version(self):
        @anydef_decorator(model=TEST_MODEL)
        def func(x: int) -> int:
            """Clear docstring."""
            pass
        assert func(input) == expected

    @pytest.mark.asyncio
    async def test_async_version(self):
        @anydef_async(model=TEST_MODEL)
        async def func(x: int) -> int:
            """Clear docstring."""
            pass
        assert await func(input) == expected
```

### Environment Variables
- `OPENAI_API_KEY`: Required for tests
- `ANYDEF_TEST_MODEL`: Override test model (default: gpt-3.5-turbo)

## Sandbox Constraints

Code running in PyodideSandbox has these limitations:

1. **No filesystem access**: Cannot use `open()`, `os.path`, etc.
2. **No network access**: Cannot use `requests`, `urllib`, etc. (unless `allow_net=True`)
3. **Standard library only**: Most stdlib works, but no pip packages inside sandbox
4. **JSON-serializable results**: Results pass through JSON, so only primitives/lists/dicts

### What Works Inside Sandbox
- All Python builtins
- `math`, `itertools`, `functools`, `collections`
- `json`, `re`, `datetime`
- Basic algorithms and data processing

### What Doesn't Work
- `import requests`
- `open('file.txt')`
- `os.system()`
- Custom pip packages

## Error Handling

```python
try:
    result = await sandbox.execute(code)
    if result.status == "error":
        raise RuntimeError(f"Sandbox error: {result.stderr}")
except openai.APIStatusError as e:
    if e.status_code == 404:
        # Model not found
    raise
```

## Dependencies

### Runtime
- `openai>=1.0.0`
- `langchain-sandbox>=0.0.6`

### System
- **Deno runtime** (required for PyodideSandbox)

## When Making Changes

1. Read existing code before modifying
2. Maintain backward compatibility for decorator API
3. Keep both sync and async versions in parity
4. Write tests for new functionality
5. Update documentation if user-facing
6. Run full test suite before committing

## Common Pitfalls

- Decorator must handle both `@anydef` and `@anydef()` syntax
- Results must be JSON-serializable (no custom objects)
- Async context detection is needed for sync decorator
- Generated code cache is per-wrapper-instance, not global
- Deno must be installed for sandbox to work
