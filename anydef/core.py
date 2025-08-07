import functools
import inspect
import openai
import os
from typing import Any, Callable, Optional

# Set your OpenAI API key here or use environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Default model to use
# Using a more widely available model as default
DEFAULT_MODEL = "gpt-3.5-turbo"


def anydef(
    func: Optional[Callable[..., Any]] = None, 
    model: str = DEFAULT_MODEL
) -> Callable[..., Any]:
    """
    A decorator that auto-generates function implementations using OpenAI's GPT models.
    
    Args:
        func: The function to be decorated. Should have a docstring describing its purpose.
        model: The OpenAI model to use for generation (default: gpt-3.5-turbo).
        
    Returns:
        A wrapper function that generates and executes the implementation.
    """
    # Handle both @anydef and @anydef() usage
    if func is None:
        # Called with arguments: @anydef(model="gpt-4")
        def decorator(f):
            return anydef(f, model)
        return decorator
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get function signature
        sig = inspect.signature(func)
        
        # Create a prompt for the AI model
        prompt = f"Generate Python code for the following function:\n\n"
        prompt += f"Function name: {func.__name__}\n"
        prompt += f"Signature: {sig}\n"
        prompt += f"Docstring: {func.__doc__}\n"
        prompt += "\nProvide only the function implementation, without any additional text or markdown formatting.\n"
        prompt += "Example output format:\n    # Implementation goes here\n    return result\n"
        
        try:
            # Call the OpenAI API to generate the implementation
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates Python function implementations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract the generated code
            generated_code = response.choices[0].message.content.strip()
            
            # Log the generated code for debugging
            print(f"Generated code for {func.__name__}:")
            print(generated_code)
            
            # Create a safe execution environment
            # We'll only allow safe built-ins and the function parameters
            safe_builtins = {
                "abs": abs,
                "all": all,
                "any": any,
                "bool": bool,
                "chr": chr,
                "divmod": divmod,
                "enumerate": enumerate,
                "filter": filter,
                "float": float,
                "int": int,
                "isinstance": isinstance,
                "len": len,
                "list": list,
                "map": map,
                "max": max,
                "min": min,
                "pow": pow,
                "range": range,
                "reversed": reversed,
                "round": round,
                "set": set,
                "slice": slice,
                "sorted": sorted,
                "str": str,
                "sum": sum,
                "tuple": tuple,
                "type": type,
                "zip": zip,
            }
            
            # Execute the generated code in a restricted environment
            local_vars = {}
            exec(generated_code, {"__builtins__": safe_builtins}, local_vars)
            
            # Call the generated function with the provided arguments
            result = local_vars[func.__name__](*args, **kwargs)
            return result
            
        except openai.APIStatusError as e:
            if e.status_code == 404:
                print(f"Error: Model '{model}' not found. Please check that the model name is correct and that you have access to it.")
                print("Available models can be found at: https://platform.openai.com/docs/models")
                print("You can specify a different model using the model parameter: @anydef(model='gpt-4')")
            else:
                print(f"OpenAI API error (status {e.status_code}): {e.message}")
            raise
        except Exception as e:
            print(f"Error generating or executing function {func.__name__}: {e}")
            raise
    
    return wrapper