# AI Service

This repository contains the AI service for our graduation project: an adaptive task manager designed to support people with ADHD.

The service uses an LLM to turn natural-language input into structured task data. For example, it can identify task titles, deadlines, durations, urgency, categories, recurring tasks, and follow-up questions when clarification is needed.

## Setup

Requirements: Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file with your LLM provider settings:

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://your-llm-provider.example/v1
LLM_MODEL=your_model_name
```

## Run an extraction example

```bash
uv run ai-service "Study fine-tuning for two hours tomorrow"
```

## Project structure

- `src/ai_service/` - configuration, LLM adapter, extraction service, prompts, and task schemas.
- `prompts/` - prompt templates used by the service.
- `evals/` - evaluation scripts for task extraction.
- `tests/` - automated tests.

## Status

This service is under active development as part of the graduation project.
