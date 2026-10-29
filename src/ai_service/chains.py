import argparse
import time

from .llm import OpenAITaskExtractor, TaskExtractor
from .prompts import FilePromptLoader, PromptLoader
from .schemas import TaskExtraction
from .settings import LLMSettings


class TaskExtractionService:
    """Coordinates prompt retrieval and task extraction for application callers."""

    def __init__(self, extractor: TaskExtractor, prompt_loader: PromptLoader) -> None:
        self._extractor = extractor
        self._prompt_loader = prompt_loader

    def extract(self, user_input: str) -> TaskExtraction:
        wrapped_input = f"<user_input>\n{user_input}\n</user_input>"
        return self._extractor.extract(self._prompt_loader.load("extract"), wrapped_input)


def create_task_extraction_service() -> TaskExtractionService:
    """Compose production dependencies at the application's boundary."""
    return TaskExtractionService(
        OpenAITaskExtractor(LLMSettings.from_environment()), FilePromptLoader()
    )


def extract_tasks(user_input: str, service: TaskExtractionService | None = None) -> TaskExtraction:
    """Extract structured tasks from natural-language input."""
    return (service or create_task_extraction_service()).extract(user_input)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract structured tasks from text.")
    parser.add_argument("text", help="Natural-language task input to extract.")
    arguments = parser.parse_args()

    started_at = time.perf_counter()
    print(extract_tasks(arguments.text).model_dump_json(indent=2))
    print(f"Execution time: {time.perf_counter() - started_at:.2f} seconds")

if __name__ == "__main__":
    main()
