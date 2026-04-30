# chat_engine

This is a small utility package used by AEGIS for building prompts and running
batch inference pipelines.

The implementation lives in `chat_engine/src/chat_engine/processor_builder.py`.

## What it provides

- Load items from one or more JSON files (typically containing image paths and metadata)
- Build OpenAI-style `messages` using a `kwargs_generator` and prompt templates
- Call a provided `inference_func` (OpenAI-compatible) for each item
- Write results and error logs to disk, organized by `namespace` and `task_name`

## Dependencies

- Python 3.12+
- `tqdm`
- `openai` (only required if you use OpenAI-compatible clients)
