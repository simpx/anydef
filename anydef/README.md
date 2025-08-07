# AnyDef Library

This is the main module of the AnyDef library.

## Modules

- `core.py`: Contains the main `@anydef` decorator implementation
- `version.py`: Contains the version information

## Usage

```python
from anydef import anydef

@anydef
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    pass

result = fibonacci(10)
print(result)  # Output: 55
```
