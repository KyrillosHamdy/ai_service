import os
from dotenv import load_dotenv
from openai import OpenAI

from .schemas import TaskExtraction

# load environment variables from .env file
load_dotenv()

# initialize OpenAI client with environment variables
_client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.environ["LLM_BASE_URL"],
    timeout=60,
    max_retries=2
)

# define the model to use for LLM
MODEL = os.getenv("LLM_MODEL", "gemma")

def extraction(
    system: str,
    user: str, 
    temperature: float = 0.0
    ) -> TaskExtraction:
    """
    extract specific information from the given prompt using the specified model.

    Args:
        prompt (str): The input prompt to generate a completion for.
        json_mode (bool): Whether to return the completion in JSON format.
        temperature (float): Sampling temperature for randomness in generation.

    Returns:
        TaskExtraction: The extracted task information.
    """
    response = _client.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {"role": "user", "content": user}
        ],
        response_format=TaskExtraction,
        temperature=temperature,
        max_tokens=1024,
    )
    message = response.choices[0].message
    
    if message.refusal:
        raise ValueError(f"Model refused extraction: {message.refusal}")

    if message.parsed is None:
        raise ValueError("No structured extraction was returned.")
    
    return message.parsed