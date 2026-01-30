# Claude Code Instructions for AnyDef

This document provides guidance for Claude Code when assisting with the AnyDef project.

## Project Context

AnyDef is a Python library that uses AI to auto-generate function implementations. Users write function signatures with docstrings, and the `@anydef` decorator generates the implementation at runtime using OpenAI's API.

### Core Usage Pattern

```python
from anydef import anydef

@anydef
def function_name(param: Type) -> ReturnType:
    """Docstring describing what the function should do."""
    pass

# The function is now callable and will generate its implementation via AI
result = function_name(arg)
```

## Key Files

| File | Purpose |
|------|---------|
| `anydef/core.py` | Main decorator implementation |
| `anydef/__init__.py` | Package exports |
| `anydef/version.py` | Version string |
| `tests/test_anydef.py` | Test suite |
| `examples/` | Usage examples |

## Code Conventions

### Style
- Use Black formatter (line length 88)
- Follow PEP 8
- Type hints required for all public functions
- Docstrings required for all public functions

### Imports Order
1. Standard library
2. Third-party packages
3. Local imports

### Naming
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: prefix with `_`

## Common Tasks

### Adding a New Parameter to `@anydef`

1. Update the `anydef()` function signature in `core.py`
2. Handle both `@anydef` and `@anydef()` decorator patterns
3. Add tests in `test_anydef.py`
4. Add example in `examples/`
5. Update README.md

### Adding a New AI Provider

1. Create provider module: `anydef/providers/{provider}.py`
2. Implement common interface
3. Update `core.py` to support provider selection
4. Add provider-specific error handling

### Modifying the Safe Execution Environment

Location: `anydef/core.py`, `safe_builtins` dictionary

When adding built-ins, consider security implications. Only add functions that:
- Cannot access the filesystem
- Cannot make network requests
- Cannot execute arbitrary code

## Testing Requirements

### Before Any Commit
```bash
black .
flake8
pytest
```

### Test Pattern
```python
def test_feature():
    @anydef(model="test-model")
    def func(x: int) -> int:
        """Clear docstring."""
        pass

    assert func(input) == expected
```

### Tests Require
- Real API key (set `OPENAI_API_KEY`)
- Network access to OpenAI

## Error Handling

The project uses specific error handling:

```python
try:
    # API call
except openai.APIStatusError as e:
    if e.status_code == 404:
        # Model not found - provide helpful message
    else:
        # Other API errors
except Exception as e:
    # General errors
```

Always provide helpful error messages that guide users to solutions.

## Security Considerations

1. **Sandboxed Execution**: Generated code runs with limited built-ins
2. **No File Access**: Generated code cannot read/write files
3. **No Network Access**: Generated code cannot make network requests
4. **Input Validation**: Validate all user inputs before processing

## Dependencies

### Production
- `openai>=1.0.0`

### Development
- `pytest>=6.0.0`
- `black>=22.0.0`
- `flake8>=4.0.0`

## When Making Changes

1. Read existing code before modifying
2. Maintain backward compatibility
3. Keep the API simple
4. Write tests for new functionality
5. Update documentation if user-facing
6. Run the full test suite before committing

## Common Pitfalls

- The decorator must handle both `@anydef` and `@anydef()` syntax
- Generated code might vary between API calls - tests should be deterministic where possible
- Model availability varies by API key - use configurable models in tests
- The `exec()` call uses a restricted environment - don't assume all Python features work

## Project Goals

1. **Simplicity**: Minimal configuration required
2. **Flexibility**: Support multiple models and providers
3. **Security**: Safe execution of generated code
4. **Developer Experience**: Clear errors and good documentation
