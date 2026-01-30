import asyncio
import functools
import inspect
import openai
import os
from typing import Any, Callable, Optional, Union

from langchain_sandbox import PyodideSandbox

# Set your OpenAI API key here or use environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Default model to use
DEFAULT_MODEL = "gpt-3.5-turbo"

# Sandbox timeout in seconds
DEFAULT_TIMEOUT = 30


async def _execute_in_sandbox(
    code: str,
    func_name: str,
    args: tuple,
    kwargs: dict,
    timeout: int = DEFAULT_TIMEOUT
) -> Any:
    """Execute generated code in PyodideSandbox and return the result."""
    sandbox = PyodideSandbox(
        allow_net=False,
        timeout=timeout,
    )

    # Build the execution code that calls the function and captures the result
    # We need to serialize args/kwargs and deserialize in the sandbox
    execution_code = f'''
{code}

# Call the function with provided arguments
import json

_args = json.loads({repr(list(args).__str__())})
_kwargs = json.loads({repr(kwargs.__str__())})
_result = {func_name}(*_args, **_kwargs)

# Output the result as JSON for parsing
print(json.dumps({{"__anydef_result__": _result}}))
'''

    result = await sandbox.execute(execution_code)

    if result.status == "error":
        raise RuntimeError(f"Sandbox execution error: {result.stderr}")

    # Parse the result from stdout
    import json
    stdout = result.stdout.strip()

    # Find the JSON result line
    for line in reversed(stdout.split('\n')):
        try:
            data = json.loads(line)
            if isinstance(data, dict) and "__anydef_result__" in data:
                return data["__anydef_result__"]
        except json.JSONDecodeError:
            continue

    raise RuntimeError(f"Failed to parse result from sandbox output: {stdout}")


def _generate_code(func: Callable, model: str) -> str:
    """Generate function implementation using OpenAI."""
    sig = inspect.signature(func)

    prompt = f"""Generate a complete Python function implementation.

Function name: {func.__name__}
Signature: {sig}
Docstring: {func.__doc__}

Requirements:
1. Provide ONLY the complete function definition starting with 'def {func.__name__}'
2. Do NOT include any markdown formatting, code blocks, or explanations
3. The function must be self-contained (no external imports except standard library)
4. Use only Python standard library features

Example format:
def {func.__name__}{sig}:
    # implementation
    return result
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a Python code generator. Output only valid Python code, no explanations."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.2  # Lower temperature for more consistent code
        )

        generated_code = response.choices[0].message.content.strip()

        # Clean up the generated code (remove markdown if present)
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
        if generated_code.startswith("```"):
            generated_code = generated_code[3:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
        generated_code = generated_code.strip()

        return generated_code

    except openai.APIStatusError as e:
        if e.status_code == 404:
            raise RuntimeError(
                f"Model '{model}' not found. Check https://platform.openai.com/docs/models "
                f"for available models. Use @anydef(model='gpt-4') to specify a different model."
            )
        raise


def anydef(
    func: Optional[Callable[..., Any]] = None,
    model: str = DEFAULT_MODEL,
    timeout: int = DEFAULT_TIMEOUT,
    debug: bool = False,
) -> Callable[..., Any]:
    """
    A decorator that auto-generates function implementations using AI and executes
    them safely in a sandboxed environment (PyodideSandbox).

    Args:
        func: The function to be decorated. Should have a docstring describing its purpose.
        model: The OpenAI model to use for generation (default: gpt-3.5-turbo).
        timeout: Sandbox execution timeout in seconds (default: 30).
        debug: If True, print the generated code for debugging.

    Returns:
        A wrapper function that generates and executes the implementation in a sandbox.

    Example:
        @anydef
        def fibonacci(n: int) -> int:
            '''Calculate the nth Fibonacci number.'''
            pass

        result = fibonacci(10)  # Returns 55
    """
    # Handle both @anydef and @anydef() usage
    if func is None:
        def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
            return anydef(f, model=model, timeout=timeout, debug=debug)
        return decorator

    # Cache for generated code
    _generated_code_cache: dict = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Generate code if not cached
        if func.__name__ not in _generated_code_cache:
            code = _generate_code(func, model)
            _generated_code_cache[func.__name__] = code

            if debug:
                print(f"Generated code for {func.__name__}:")
                print(code)
                print("-" * 40)

        code = _generated_code_cache[func.__name__]

        # Execute in sandbox
        try:
            # Check if we're already in an async context
            try:
                loop = asyncio.get_running_loop()
                # We're in an async context, need to use a different approach
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run,
                        _execute_in_sandbox(code, func.__name__, args, kwargs, timeout)
                    )
                    return future.result()
            except RuntimeError:
                # No running loop, we can use asyncio.run directly
                return asyncio.run(
                    _execute_in_sandbox(code, func.__name__, args, kwargs, timeout)
                )
        except Exception as e:
            raise RuntimeError(f"Error executing {func.__name__}: {e}") from e

    return wrapper


# Async version of the decorator
def anydef_async(
    func: Optional[Callable[..., Any]] = None,
    model: str = DEFAULT_MODEL,
    timeout: int = DEFAULT_TIMEOUT,
    debug: bool = False,
) -> Callable[..., Any]:
    """
    Async version of anydef decorator for use in async contexts.

    Example:
        @anydef_async
        async def fibonacci(n: int) -> int:
            '''Calculate the nth Fibonacci number.'''
            pass

        result = await fibonacci(10)  # Returns 55
    """
    if func is None:
        def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
            return anydef_async(f, model=model, timeout=timeout, debug=debug)
        return decorator

    _generated_code_cache: dict = {}

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        if func.__name__ not in _generated_code_cache:
            code = _generate_code(func, model)
            _generated_code_cache[func.__name__] = code

            if debug:
                print(f"Generated code for {func.__name__}:")
                print(code)
                print("-" * 40)

        code = _generated_code_cache[func.__name__]
        return await _execute_in_sandbox(code, func.__name__, args, kwargs, timeout)

    return wrapper
