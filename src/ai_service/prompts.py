from pathlib import Path
from typing import Protocol


class PromptLoader(Protocol):
    """Port for retrieving a named system prompt."""

    def load(self, prompt_name: str) -> str:
        """Return the prompt content for the given name."""


class FilePromptLoader:
    """Loads version-controlled Markdown prompts from disk."""

    def __init__(self, prompts_dir: Path | None = None) -> None:
        self._prompts_dir = prompts_dir or Path(__file__).resolve().parents[2] / "prompts"

    def load(self, prompt_name: str) -> str:
        return (self._prompts_dir / f"{prompt_name}.md").read_text(encoding="utf-8")
