from __future__ import annotations

import base64
import json
import mimetypes
import os
from functools import lru_cache
from typing import Any, List, Tuple


def random_generate_question(content, choose):
    import random

    # Create an independent RNG instance
    local_random = random.Random()
    local_random.shuffle(content)
    paired = list(zip(content, choose))
    pair_dict = dict(paired)
    options_block = "\n".join([f"{letter}. {text}" for text, letter in paired])
    return pair_dict, options_block


def image2base64(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("Unsupported or unrecognized image format.")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"


def infer_dataset_category_from_path(path: str) -> str:
    search_index = {
        "image_inference_forgery": "image_inference_forgery",
        "real": "real",
        "targeted_region_editing": "targeted_region_editing",
        "targeted_region_restoration": "targeted_region_restoration",
        "text_constraint_fabrication": "text_constraint_fabrication",
    }
    for key, value in search_index.items():
        if key in path:
            return value
    raise ValueError(f"Failed to infer dataset category from path: {path}")


def infer_answer_from_path(path: str, answer_json_path: str) -> str:
    with open(answer_json_path, "r", encoding="utf-8") as f:
        search_index = json.load(f)
    for key, value in search_index.items():
        if (key in path) or (key == path):
            return value
    raise ValueError(f"Failed to find answer for {path} in {answer_json_path}")


def get_caption_from_path(path: str, search_json_paths: List[str]) -> str:
    for search_json_path in search_json_paths:
        with open(search_json_path, "r", encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            if item.get("image_path") in path:
                return item["original_caption"]
    raise ValueError(f"Failed to find caption for: {path}")


@lru_cache(maxsize=1)
def get_vec_query(
    db_path: str = "assets/dataset_with_vector_index.db",
    model_path: str = "assets/facebook/dinov3-vits16-pretrain-lvd1689m",
):
    """
    Lazily create the vector retrieval client for few-shot reference selection.

    This is intentionally lazy to keep the benchmark importable in environments
    where the retrieval assets (DB/model) are not present.
    """
    try:
        from query_engine import VecQuery
    except ImportError as e:
        raise ImportError(
            "Few-shot retrieval requires the vendored `query-engine` package. "
            "Install the benchmark dependencies and ensure query-engine is available."
        ) from e

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Vector index DB not found: {db_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Embedder model path not found: {model_path}")

    return VecQuery(db_path, model_path)

