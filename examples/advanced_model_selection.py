from anydef import anydef

# Using the default model (gpt-3.5-turbo)
@anydef
def fibonacci_default(n: int) -> int:
    """Calculate the nth Fibonacci number using the default model."""
    pass

# Specifying a specific model
@anydef(model="gpt-4")
def fibonacci_gpt4(n: int) -> int:
    """Calculate the nth Fibonacci number using GPT-4."""
    pass

# You can also specify other available models
# @anydef(model="gpt-4-turbo")
# def fibonacci_gpt4_turbo(n: int) -> int:
#     """Calculate the nth Fibonacci number using GPT-4 Turbo."""
#     pass

if __name__ == "__main__":
    n = 10
    print(f"Using default model:")
    result = fibonacci_default(n)
    print(f"The {n}th Fibonacci number is: {result}")
    
    print(f"\nUsing GPT-4 model:")
    result = fibonacci_gpt4(n)
    print(f"The {n}th Fibonacci number is: {result}")