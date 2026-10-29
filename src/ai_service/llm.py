from typing import Protocol

from openai import OpenAI

from .schemas import TaskExtraction
from .settings import LLMSettings


class TaskExtractor(Protocol):
    """Port used by the application layer to extract structured tasks."""

    def extract(self, system_prompt: str, user_input: str) -> TaskExtraction:
        """Extract task data from a system prompt and user input."""


class OpenAITaskExtractor:
    """OpenAI-compatible implementation of the task-extraction port."""

    def __init__(self, settings: LLMSettings, client: OpenAI | None = None) -> None:
        self._settings = settings
        self._client = client or OpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
            timeout=settings.timeout_seconds,
            max_retries=settings.max_retries,
        )

    def extract(self, system_prompt: str, user_input: str) -> TaskExtraction:
        response = self._client.chat.completions.parse(
            model=self._settings.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            response_format=TaskExtraction,
            temperature=self._settings.temperature,
            max_tokens=self._settings.max_tokens,
        )
        message = response.choices[0].message

        if message.refusal:
            raise ValueError(f"Model refused extraction: {message.refusal}")
        if message.parsed is None:
            raise ValueError("No structured extraction was returned.")

        return message.parsed
