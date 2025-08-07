# API Reference

## `anydef.anydef`

```python
def anydef(func: Callable[..., Any]) -> Callable[..., Any]:
```

A decorator that auto-generates function implementations using OpenAI's GPT models.

### Parameters

- `func` (Callable[..., Any]): The function to be decorated. Should have a docstring describing its purpose.

### Returns

- `Callable[..., Any]`: A wrapper function that generates and executes the implementation.

### Example

```python
from anydef import anydef

@anydef
def multiply(x: int, y: int) -> int:
    """Multiply two integers."""
    pass

result = multiply(4, 5)
print(result)  # Output: 20
```