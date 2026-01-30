import os
import sys
import pytest

# Add the parent directory to the path so we can import anydef
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import anydef
from anydef import anydef as anydef_decorator, anydef_async

# Default model for tests - can be overridden via environment variable
TEST_MODEL = os.getenv("ANYDEF_TEST_MODEL", "gpt-3.5-turbo")


class TestAnydefSync:
    """Test synchronous anydef decorator."""

    def test_fibonacci(self):
        """Test the fibonacci function."""
        @anydef_decorator(model=TEST_MODEL, debug=True)
        def fibonacci(n: int) -> int:
            """Calculate the nth Fibonacci number."""
            pass

        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(10) == 55

    def test_factorial(self):
        """Test factorial function."""
        @anydef_decorator(model=TEST_MODEL)
        def factorial(n: int) -> int:
            """Calculate the factorial of a number. factorial(0) = 1."""
            pass

        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120

    def test_is_prime(self):
        """Test prime number checker."""
        @anydef_decorator(model=TEST_MODEL)
        def is_prime(n: int) -> bool:
            """Check if a number is prime. Return True if prime, False otherwise."""
            pass

        assert is_prime(2) == True
        assert is_prime(17) == True
        assert is_prime(4) == False
        assert is_prime(1) == False

    def test_reverse_words(self):
        """Test string reversal function."""
        @anydef_decorator(model=TEST_MODEL)
        def reverse_words(text: str) -> str:
            """Reverse the order of words in a string. Example: 'Hello World' -> 'World Hello'."""
            pass

        assert reverse_words("Hello World") == "World Hello"
        assert reverse_words("one two three") == "three two one"

    def test_count_vowels(self):
        """Test vowel counting function."""
        @anydef_decorator(model=TEST_MODEL)
        def count_vowels(text: str) -> int:
            """Count the number of vowels (a, e, i, o, u) in a string, case insensitive."""
            pass

        assert count_vowels("Hello World") == 3
        assert count_vowels("aeiou") == 5
        assert count_vowels("xyz") == 0


class TestAnydefAsync:
    """Test asynchronous anydef_async decorator."""

    @pytest.mark.asyncio
    async def test_fibonacci_async(self):
        """Test async fibonacci function."""
        @anydef_async(model=TEST_MODEL, debug=True)
        async def fibonacci(n: int) -> int:
            """Calculate the nth Fibonacci number."""
            pass

        assert await fibonacci(0) == 0
        assert await fibonacci(1) == 1
        assert await fibonacci(10) == 55

    @pytest.mark.asyncio
    async def test_factorial_async(self):
        """Test async factorial function."""
        @anydef_async(model=TEST_MODEL)
        async def factorial(n: int) -> int:
            """Calculate the factorial of a number. factorial(0) = 1."""
            pass

        assert await factorial(5) == 120


class TestDecorationStyles:
    """Test different decorator usage styles."""

    def test_decorator_without_parentheses(self):
        """Test @anydef without parentheses."""
        @anydef_decorator
        def add(a: int, b: int) -> int:
            """Add two numbers together."""
            pass

        assert add(2, 3) == 5

    def test_decorator_with_empty_parentheses(self):
        """Test @anydef() with empty parentheses."""
        @anydef_decorator()
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers together."""
            pass

        assert multiply(3, 4) == 12

    def test_decorator_with_model_parameter(self):
        """Test @anydef(model=...) with model specified."""
        @anydef_decorator(model=TEST_MODEL)
        def subtract(a: int, b: int) -> int:
            """Subtract b from a."""
            pass

        assert subtract(10, 3) == 7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
