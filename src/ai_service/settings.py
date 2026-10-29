import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class LLMSettings:
    """Configuration for an OpenAI-compatible LLM provider."""

    api_key: str
    base_url: str
    model: str = "gemma"
    timeout_seconds: float = 60.0
    max_retries: int = 2
    temperature: float = 0.0
    max_tokens: int = 1024

    @classmethod
    def from_environment(cls) -> "LLMSettings":
        """Load settings when the application is composed, not on import."""
        load_dotenv()
        try:
            api_key = os.environ["LLM_API_KEY"]
            base_url = os.environ["LLM_BASE_URL"]
        except KeyError as error:
            raise RuntimeError(f"Missing required environment variable: {error.args[0]}") from error

        return cls(api_key=api_key, base_url=base_url, model=os.getenv("LLM_MODEL", "gemma"))
