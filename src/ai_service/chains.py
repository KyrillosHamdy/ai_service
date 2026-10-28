from pathlib import Path
import time

from .llm import extraction

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"

def load_prompt(prompt_name: str) -> str:
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
    return prompt_path.read_text()

def extract_tasks(user_input: str) -> dict:
    user_input = f'<user_input>\n{user_input}\n</user_input>'
    system_prompt = load_prompt("extract")
    return user_input, extraction(system_prompt, user_input)

if __name__ == "__main__":
    t = time.perf_counter()
    print(extract_tasks("study finetuning for 2 hours tomorrow and then go to the gym on Monday and Wednesday"))
    print(f"Execution time: {time.perf_counter() - t:.2f} seconds")