from anydef import anydef

# Using a specific model that should be available
@anydef(model="pre-qwen3-coder-chat-prompt-caching")
def reverse_words(text: str) -> str:
    """Reverse the order of words in a string."""
    pass

@anydef(model="pre-qwen3-coder-chat-prompt-caching")
def count_vowels(text: str) -> int:
    """Count the number of vowels in a string."""
    pass

if __name__ == "__main__":
    text = "Hello World"
    print(f"Original text: {text}")
    print(f"Reversed words: {reverse_words(text)}")
    print(f"Vowel count: {count_vowels(text)}")