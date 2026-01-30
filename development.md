# AnyDef Development Guide

## Project Overview

AnyDef is a Python library that uses AI to auto-generate function implementations based on their signatures and docstrings. The core idea is simple: write a function signature with a docstring, and let AI generate the actual implementation at runtime.

## Project Structure

```
anydef/
├── anydef/                 # Main package
│   ├── __init__.py         # Package exports
│   ├── core.py             # Core decorator implementation
│   ├── version.py          # Version information
│   └── __main__.py         # CLI entry point
├── tests/                  # Test suite
│   └── test_anydef.py      # Unit tests
├── examples/               # Usage examples
│   ├── basic_fibonacci.py
│   ├── math_functions.py
│   ├── string_processing.py
│   └── advanced_model_selection.py
├── docs/                   # Documentation
│   ├── api_reference.md
│   ├── contributing.md
│   └── core_concepts.md
├── setup.py                # Package setup
├── pyproject.toml          # Project configuration
├── requirements.txt        # Production dependencies
└── requirements-dev.txt    # Development dependencies
```

## Quick Start

### 1. Clone and Setup

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

### 2. Configure API Key

```bash
export OPENAI_API_KEY=your_api_key_here
```

### 3. Run Tests

```bash
pytest tests/
```

## Core Architecture

### The `@anydef` Decorator

The decorator in `anydef/core.py` works as follows:

1. **Function Introspection**: Extracts function name, signature, and docstring
2. **Prompt Generation**: Builds a prompt for the AI model
3. **API Call**: Sends the prompt to OpenAI's API
4. **Code Execution**: Executes the generated code in a sandboxed environment
5. **Result Return**: Returns the function result

### Key Components

```python
# Decorator usage patterns
@anydef                           # Default model (gpt-3.5-turbo)
@anydef()                         # Same as above
@anydef(model="gpt-4")            # Custom model
```

### Security: Safe Execution Environment

The generated code runs in a restricted environment with limited built-ins:
- Basic types: `int`, `float`, `str`, `bool`, `list`, `dict`, `set`, `tuple`
- Iterators: `range`, `enumerate`, `zip`, `map`, `filter`, `reversed`
- Math: `abs`, `pow`, `round`, `min`, `max`, `sum`, `divmod`
- Utilities: `len`, `sorted`, `all`, `any`, `isinstance`, `type`

## Development Workflow

### Code Style

We use Black for formatting and Flake8 for linting:

```bash
# Format code
black .

# Check linting
flake8

# Both before commit
black . && flake8
```

Configuration in `pyproject.toml`:
- Line length: 88
- Target Python: 3.8+

### Running Tests

```bash
# All tests
pytest

# Verbose output
pytest -v

# Specific test
pytest tests/test_anydef.py::test_fibonacci

# With coverage
pytest --cov=anydef
```

### Adding New Features

1. Create a feature branch
2. Write tests first (TDD recommended)
3. Implement the feature in `anydef/core.py`
4. Update `__init__.py` if adding new exports
5. Add examples in `examples/`
6. Update documentation

## API Design Principles

1. **Simple by Default**: `@anydef` should work without configuration
2. **Configurable When Needed**: Support model selection and other options
3. **Fail Gracefully**: Clear error messages with guidance
4. **Secure**: Sandboxed execution environment

## Testing Guidelines

### Test Structure

```python
def test_feature_name():
    """Describe what the test verifies."""
    @anydef(model="your-model")
    def function_to_test(param: Type) -> ReturnType:
        """Clear docstring describing behavior."""
        pass

    # Assertions
    assert function_to_test(input) == expected_output
```

### Test Categories

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test with actual API calls
- **Error Handling Tests**: Test error scenarios

## Debugging

### Enable Debug Output

The decorator prints generated code by default. For more debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **Model Not Found**: Check model name and API access
2. **API Key Invalid**: Verify `OPENAI_API_KEY` environment variable
3. **Generated Code Error**: Check docstring clarity

## Release Process

1. Update version in `anydef/version.py` and `setup.py`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create git tag: `git tag v0.x.x`
5. Build: `python -m build`
6. Upload: `twine upload dist/*`

## Future Roadmap

- [ ] Caching generated implementations
- [ ] Support for multiple AI providers (Anthropic, etc.)
- [ ] Async function support
- [ ] Type validation for generated code
- [ ] Configuration file support
