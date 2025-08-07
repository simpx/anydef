# Core Concepts

The `@anydef` decorator is designed to automatically generate function implementations based on their signature and docstring. It uses OpenAI's GPT models to understand the intended functionality and create the corresponding Python code.

## How it Works

1. When a function decorated with `@anydef` is called, the decorator intercepts the call.
2. It analyzes the function's signature (name, parameters, return type) and docstring.
3. It constructs a prompt for the OpenAI API, asking it to generate the function implementation.
4. The generated code is then executed in a restricted environment.
5. The result of the generated function is returned to the caller.

## Example

```python
from anydef import anydef

@anydef
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    pass

result = add_numbers(5, 3)
print(result)  # Output: 8
```

In this example, even though the function body is just `pass`, the `@anydef` decorator will generate the actual implementation using AI.

## Security Considerations

Executing AI-generated code can be risky. The current implementation uses a restricted execution environment, but it's recommended to carefully review any generated code before using it in production environments. Future versions may include more robust sandboxing mechanisms.