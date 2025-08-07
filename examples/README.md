# AnyDef Examples

This directory contains example scripts demonstrating how to use the AnyDef library.

## Basic Usage

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

## Specifying a Model

You can specify which OpenAI model to use for generating the function implementation:

```python
from anydef import anydef

@anydef(model="gpt-4")
def fibonacci_gpt4(n: int) -> int:
    """Calculate the nth Fibonacci number using GPT-4."""
    pass

result = fibonacci_gpt4(10)
print(result)  # Output: 55
```

## More Complex Examples

### Mathematical Functions

```python
from anydef import anydef

@anydef
def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    pass

@anydef
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    pass

print(factorial(5))  # Output: 120
print(is_prime(17))  # Output: True
```

### String Processing

```python
from anydef import anydef

@anydef
def reverse_words(text: str) -> str:
    """Reverse the order of words in a string."""
    pass

@anydef
def count_vowels(text: str) -> int:
    """Count the number of vowels in a string."""
    pass

print(reverse_words("Hello World"))  # Output: "World Hello"
print(count_vowels("Hello World"))   # Output: 3
```

## Running the Examples

To run these examples, you need to:

1. Install the AnyDef library:
   ```bash
   pip install anydef
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

3. Copy the example code into a Python file and run it.
