from anydef import anydef

# Using a specific model that should be available
@anydef(model="pre-qwen3-coder-chat-prompt-caching")
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    pass

if __name__ == "__main__":
    # This will automatically generate and execute the Fibonacci function
    result = fibonacci(10)
    print(f"The 10th Fibonacci number is: {result}")