import unittest

from ai_service.chains import TaskExtractionService, extract_tasks
from ai_service.schemas import ExtractedTask, TaskExtraction


class StubExtractor:
    def __init__(self) -> None:
        self.system_prompt: str | None = None
        self.user_input: str | None = None

    def extract(self, system_prompt: str, user_input: str) -> TaskExtraction:
        self.system_prompt = system_prompt
        self.user_input = user_input
        return TaskExtraction(tasks=[ExtractedTask(title="Buy milk")])


class StubPromptLoader:
    def load(self, prompt_name: str) -> str:
        if prompt_name != "extract":
            raise AssertionError("Unexpected prompt requested")
        return "system prompt"


class TaskExtractionServiceTests(unittest.TestCase):
    def test_extract_returns_domain_model_and_wraps_input(self) -> None:
        extractor = StubExtractor()
        service = TaskExtractionService(extractor, StubPromptLoader())

        result = extract_tasks("Buy milk", service)

        self.assertIsInstance(result, TaskExtraction)
        self.assertEqual(result.tasks[0].title, "Buy milk")
        self.assertEqual(extractor.system_prompt, "system prompt")
        self.assertEqual(extractor.user_input, "<user_input>\nBuy milk\n</user_input>")


if __name__ == "__main__":
    unittest.main()
