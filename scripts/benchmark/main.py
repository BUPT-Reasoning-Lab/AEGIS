from __future__ import annotations

import argparse
import json
import os
import random
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union


Json = Union[dict, list]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _repo_root_from_here() -> Path:
    # .../scripts/benchmark/main.py -> repo root is 2 levels up from scripts/
    return Path(__file__).resolve().parents[2]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _safe_format(template: str, mapping: Dict[str, Any]) -> str:
    # Raise a clear error if placeholders are missing.
    try:
        return template.format_map(mapping)
    except KeyError as e:
        missing = str(e).strip("'")
        raise KeyError(f"Missing template variable: {missing}") from e


def _build_openai_messages(
    system_prompt: str,
    user_prompt: str,
    images_data_urls: List[str],
) -> List[Dict[str, Any]]:
    user_content: List[Dict[str, Any]] = [{"type": "text", "text": user_prompt}]
    for url in images_data_urls:
        user_content.append({"type": "image_url", "image_url": {"url": url}})

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def _load_json(path: Path) -> Json:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _iter_dataset_items(dataset_json_path: Path) -> Iterable[dict]:
    data = _load_json(dataset_json_path)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                yield item
    elif isinstance(data, dict):
        # Some datasets store as dict keyed by id; normalize to list of dicts.
        for _, item in data.items():
            if isinstance(item, dict):
                yield item


def _select_prompt_from_dir(prompt_dir: Path, item: dict) -> Path:
    """
    Select a per-scenario user prompt file from a directory.

    CoT prompts are stored as:
      prompt/user/<task>.md/<Scenario>.md
    """
    # 1) Try explicit fields first
    for key in ("scenario", "domain", "category", "scene", "type"):
        v = item.get(key)
        if isinstance(v, str) and v.strip():
            cand = prompt_dir / f"{v.strip()}.md"
            if cand.exists():
                return cand

    # 2) Heuristic from image path if available
    img = item.get("image_path") or ""
    img_lower = str(img).lower()
    heuristic_map = [
        ("micrograph", "Micrograph.md"),
        ("medical", "Medical_Imaging.md"),
        ("stained", "Stained_Micrograph.md"),
        ("diagram", "Diagram.md"),
        ("chart", "Chart.md"),
        ("physical", "Physical_Object.md"),
    ]
    for needle, fname in heuristic_map:
        if needle in img_lower:
            cand = prompt_dir / fname
            if cand.exists():
                return cand

    # 3) Default
    default = prompt_dir / "Others.md"
    if default.exists():
        return default

    # 4) Last resort: pick any .md
    md_files = sorted([p for p in prompt_dir.glob("*.md") if p.is_file()])
    if not md_files:
        raise FileNotFoundError(f"No markdown prompts found in directory: {prompt_dir}")
    return md_files[0]


def _resolve_image_path(repo_root: Path, base_folder: str, item: dict) -> Optional[Path]:
    p = item.get("image_path") or item.get("path") or item.get("image") or item.get("img")
    if not p:
        return None
    p = str(p)
    # If already absolute, keep.
    if os.path.isabs(p):
        return Path(p)
    # Prefer repo_root/base_folder/...
    return repo_root / base_folder / p


@dataclass(frozen=True)
class TaskTypeParam:
    name: str
    sys_prompt_path: Path
    usr_prompt_path: Path
    input_json_paths: List[Path]
    base_folder: str
    kwargs_generator: Callable[[str], Dict[str, Any]]
    output_folder: str
    random_seed: int
    image_filter: Optional[Callable[[dict], bool]] = None


def _load_task_params(repo_root: Path, config_module: Any, task_names: List[str]) -> Dict[str, TaskTypeParam]:
    out: Dict[str, TaskTypeParam] = {}
    params: Dict[str, dict] = config_module.TASK_TYPE_PARAMS
    for task in task_names:
        if task not in params:
            raise ValueError(f"Unknown task: {task}. Available: {sorted(params.keys())}")
        p = params[task]
        out[task] = TaskTypeParam(
            name=task,
            sys_prompt_path=Path(p["sys_prompt_template_path"]).resolve(),
            usr_prompt_path=Path(p["user_prompt_template_path"]).resolve(),
            input_json_paths=[(repo_root / x).resolve() for x in p["input_json_paths"]],
            base_folder=p.get("base_folder", "assets"),
            kwargs_generator=p["kwargs_generator"],
            output_folder=p.get("output_folder", "results"),
            random_seed=int(p.get("random_seed", 42)),
            image_filter=p.get("image_filter"),
        )
    return out


def _select_items(
    items: List[dict],
    sample_rate: float,
    rng: random.Random,
) -> List[dict]:
    if sample_rate >= 1:
        return items
    if sample_rate <= 0:
        return []
    chosen = [it for it in items if rng.random() < sample_rate]
    return chosen


def _get_inference_func(model_entry: dict, task: str) -> Callable[[List[Dict[str, Any]]], Any]:
    inf = model_entry["inference_func"]
    if callable(inf):
        return inf
    if isinstance(inf, dict):
        if task not in inf:
            raise ValueError(f'Model "{model_entry["namespace"]}" has no inference_func for task "{task}"')
        return inf[task]
    raise TypeError("Invalid inference_func type; expected callable or dict of callables.")


def _get_sample_rate(model_entry: dict, task: str) -> float:
    sr = model_entry.get("sample_rate", 1.0)
    if isinstance(sr, dict):
        return float(sr.get(task, 1.0))
    return float(sr)


def _run_task(
    repo_root: Path,
    task_param: TaskTypeParam,
    model_entry: dict,
    max_items: Optional[int],
    dry_run: bool,
) -> Tuple[int, int]:
    sys_template = _read_text(task_param.sys_prompt_path)

    rng = random.Random(task_param.random_seed)
    n_ok = 0
    n_total = 0

    for dataset_json in task_param.input_json_paths:
        if not dataset_json.exists():
            print(
                f"[WARN] Dataset JSON not found, skipping: {dataset_json}",
                file=sys.stderr,
            )
            continue

        dataset_items = list(_iter_dataset_items(dataset_json))
        if task_param.image_filter is not None:
            dataset_items = [it for it in dataset_items if task_param.image_filter(it)]

        sample_rate = _get_sample_rate(model_entry, task_param.name)
        selected = _select_items(dataset_items, sample_rate=sample_rate, rng=rng)
        if max_items is not None:
            selected = selected[: max_items]

        for item in selected:
            n_total += 1

            # User prompt may be a directory (CoT per-scenario prompts)
            if task_param.usr_prompt_path.is_dir():
                usr_prompt_path = _select_prompt_from_dir(task_param.usr_prompt_path, item)
                usr_template = _read_text(usr_prompt_path)
            else:
                usr_template = _read_text(task_param.usr_prompt_path)

            image_path = _resolve_image_path(repo_root, task_param.base_folder, item)
            if image_path is None:
                print(
                    f"[WARN] Missing image path field in dataset item, skipping: {dataset_json}",
                    file=sys.stderr,
                )
                continue
            if not image_path.exists():
                print(
                    f"[WARN] Image file not found, skipping: {image_path}",
                    file=sys.stderr,
                )
                continue
            image_path_str = str(image_path)
            kwargs = task_param.kwargs_generator(image_path_str)

            images = kwargs.get("images", [])
            if not isinstance(images, list):
                raise TypeError("kwargs_generator must return `images` as a list of data URLs.")

            # Render prompts with remaining kwargs (excluding images/record_params)
            fmt_kwargs = {k: v for k, v in kwargs.items() if k not in {"images", "record_params"}}
            system_prompt = _safe_format(sys_template, fmt_kwargs)
            user_prompt = _safe_format(usr_template, fmt_kwargs)

            if dry_run:
                n_ok += 1
                continue

            messages = _build_openai_messages(system_prompt, user_prompt, images)
            inference = _get_inference_func(model_entry, task_param.name)

            row: Dict[str, Any] = {
                "ts": _utc_now_iso(),
                "namespace": model_entry["namespace"],
                "task": task_param.name,
                "dataset_json": str(dataset_json),
                "image_path": image_path_str,
                "record_params": kwargs.get("record_params", {}),
            }

            try:
                result = inference(messages)
                row["result"] = result
                row["status"] = "ok"
                n_ok += 1
            except Exception as e:
                row["status"] = "error"
                row["error"] = repr(e)

            out_dir = repo_root / task_param.output_folder / model_entry["namespace"] / task_param.name
            out_path = out_dir / f"{dataset_json.stem}.jsonl"
            _write_jsonl(out_path, [row])

    return n_ok, n_total


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AEGIS benchmark runner")
    p.add_argument(
        "--suite",
        default="basic",
        choices=["basic", "few_shot", "cot"],
        help="Benchmark suite to run (currently only: basic).",
    )
    p.add_argument(
        "--tasks",
        default="all",
        help='Comma-separated tasks to run (e.g. "forgeryscope,visualtext"), or "all".',
    )
    p.add_argument(
        "--models",
        default="all",
        help='Comma-separated model namespaces to run (e.g. "openai/gpt-5-pro"), or "all".',
    )
    p.add_argument("--max-items", type=int, default=None, help="Max sampled items per dataset JSON.")
    p.add_argument("--dry-run", action="store_true", help="Only validate loading and prompt rendering.")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    repo_root = _repo_root_from_here()

    if args.suite == "basic":
        from benchmark.basic import basic_config as cfg
    elif args.suite == "few_shot":
        from benchmark.few_shot import few_shot_config as cfg
    elif args.suite == "cot":
        from benchmark.CoT import cot_config as cfg
    else:
        raise ValueError(f"Unknown suite: {args.suite}")

    all_tasks = sorted(cfg.TASK_TYPE_PARAMS.keys())
    tasks = all_tasks if args.tasks == "all" else [t.strip() for t in args.tasks.split(",") if t.strip()]
    task_params = _load_task_params(repo_root, cfg, tasks)

    # Filter models
    models: List[dict] = list(cfg.TASK_LIST)
    if args.models != "all":
        wanted = {m.strip() for m in args.models.split(",") if m.strip()}
        models = [m for m in models if m.get("namespace") in wanted]
        missing = sorted(wanted - {m.get("namespace") for m in models})
        if missing:
            raise ValueError(f"Unknown model namespaces: {missing}")

    # Run
    total_ok = 0
    total_n = 0
    for model_entry in models:
        for task_name in tasks:
            ok, n = _run_task(
                repo_root=repo_root,
                task_param=task_params[task_name],
                model_entry=model_entry,
                max_items=args.max_items,
                dry_run=args.dry_run,
            )
            total_ok += ok
            total_n += n

    print(
        json.dumps(
            {
                "suite": args.suite,
                "tasks": tasks,
                "models": [m["namespace"] for m in models],
                "dry_run": bool(args.dry_run),
                "ok": total_ok,
                "total": total_n,
                "repo_root": str(repo_root),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

