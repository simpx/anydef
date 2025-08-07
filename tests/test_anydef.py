import os
import sys

# Add the parent directory to the path so we can import anydef
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import anydef

def test_fibonacci():
    """Test the fibonacci function."""
    @anydef.anydef(model="pre-qwen3-coder-chat-prompt-caching")
    def fibonacci(n: int) -> int:
        """Calculate the nth Fibonacci number."""
        pass
    
    # Test cases
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    
    print("All Fibonacci tests passed!")

def test_math_functions():
    """Test mathematical functions."""
    @anydef.anydef(model="pre-qwen3-coder-chat-prompt-caching")
    def factorial(n: int) -> int:
        """Calculate the factorial of a number."""
        pass
    
    @anydef.anydef(model="pre-qwen3-coder-chat-prompt-caching")
    def is_prime(n: int) -> bool:
        """Check if a number is prime."""
        pass
    
    # Test cases
    assert factorial(5) == 120
    assert is_prime(17) == True
    assert is_prime(4) == False
    
    print("All math function tests passed!")

def test_string_functions():
    """Test string processing functions."""
    @anydef.anydef(model="pre-qwen3-coder-chat-prompt-caching")
    def reverse_words(text: str) -> str:
        """Reverse the order of words in a string."""
        pass
    
    @anydef.anydef(model="pre-qwen3-coder-chat-prompt-caching")
    def count_vowels(text: str) -> int:
        """Count the number of vowels in a string."""
        pass
    
    # Test cases
    assert reverse_words("Hello World") == "World Hello"
    assert count_vowels("Hello World") == 3
    
    print("All string function tests passed!")

if __name__ == "__main__":
    test_fibonacci()
    test_math_functions()
    test_string_functions()
    print("All tests passed!")