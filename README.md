# AnyDef

A Python library that uses AI to auto-generate function implementations based on their signatures and docstrings.

## Installation

```bash
pip install anydef
```

## Usage

To use AnyDef, you need to set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Then, decorate your functions with `@anydef`:

```python
from anydef import anydef

@anydef
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    pass

# This will automatically generate and execute the Fibonacci function
result = fibonacci(10)
print(result)  # Output: 55
```

### Specifying a Model

By default, AnyDef uses `gpt-3.5-turbo`. You can specify a different model:

```python
from anydef import anydef

@anydef(model="gpt-4")
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    pass
```

### Handling Model Availability Issues

If you encounter a "model not found" error, it means the specified model is not available in your OpenAI account. The error message will provide guidance on how to resolve this:

```
Error: Model 'gpt-3.5-turbo' not found. Please check that the model name is correct and that you have access to it.
Available models can be found at: https://platform.openai.com/docs/models
You can specify a different model using the model parameter: @anydef(model='gpt-4')
```

In such cases, you can either:
1. Choose a different model that you have access to
2. Check the [OpenAI documentation](https://platform.openai.com/docs/models) for available models

## Requirements

- Python 3.8 or higher
- An OpenAI API key

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.