# AEGIS Benchmark

This folder contains the benchmark runner and prompt/config definitions for AEGIS.

The layout and installation workflow follow a lightweight, reproducible structure
based on `uv` dependency groups.

## Installation

From the repository root:

```bash
python -m venv .venv
. .venv/bin/activate
pip install uv
UV_CACHE_DIR="$(pwd)/.uv-cache" uv sync --group benchmark
```

### Few-shot Suite (Optional)

The few-shot suite uses a retrieval engine (`query-engine`) to select reference images.
This dependency can be heavy. Install it only if you plan to run `--suite few_shot`:

```bash
UV_CACHE_DIR="$(pwd)/.uv-cache" uv sync --group few-shot
```

## Environment Variables

Configure API keys as needed:

- `OPENROUTER_API_KEY`
- `ALI_API_KEY`
- `ZHIPU_API_KEY`
- `BYTE_API_KEY`

## Quick Sanity Check (no API calls)

Validate dataset loading and prompt rendering without calling any model.

Note: the `basic` suite expects dataset JSONs under `assets/dataset/*.json` and image
paths under `assets/`. Make sure `assets/` exists in the repository root before
running a full benchmark.

```bash
PYTHONPATH=./scripts python -m benchmark.main --suite basic --dry-run --max-items 2
```

## Run Benchmark

Run all tasks and all configured models (will make API calls):

```bash
PYTHONPATH=./scripts python -m benchmark.main --suite basic
```

Run the CoT suite:

```bash
PYTHONPATH=./scripts python -m benchmark.main --suite cot
```

Run the few-shot suite (requires `uv sync --group few-shot` and retrieval assets):

```bash
PYTHONPATH=./scripts python -m benchmark.main --suite few_shot
```

Run a subset of tasks:

```bash
PYTHONPATH=./scripts python -m benchmark.main --suite basic --tasks forgeryscope,visualtext
```

Run a specific model namespace:

```bash
PYTHONPATH=./scripts python -m benchmark.main --suite basic --models openai/gpt-5.1
```

## Outputs

Results are written under `results/` (relative to the repository root) as JSONL files:

```
results/<namespace>/<task>/<dataset_name>.jsonl
```

Each JSONL row includes `record_params` from the task kwargs generator, the parsed model
`result` (if successful), or an `error` string otherwise.

