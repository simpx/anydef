from anydef import anydef

# Using a specific model that should be available
@anydef(model="pre-qwen3-coder-chat-prompt-caching")
def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    pass

@anydef(model="pre-qwen3-coder-chat-prompt-caching")
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    pass

if __name__ == "__main__":
    print(f"Factorial of 5: {factorial(5)}")
    print(f"Is 17 prime? {is_prime(17)}")