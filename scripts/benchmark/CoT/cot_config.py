from __future__ import annotations

from benchmark.basic.model_generator import *
from benchmark.basic.task_kwargs import *
from .prompt import *


RANDOM_SEED = 42
OUTPUT_FOLDER = "results_cot"


def lazy_inference(factory, /, **factory_kwargs):
    """Defer inference client creation until the first call."""

    _fn = None

    def _call(messages):
        nonlocal _fn
        if _fn is None:
            _fn = factory(**factory_kwargs)
        return _fn(messages)

    return _call


# CoT prompts are split into:
# - system prompt files: prompt/system/*.md
# - user prompt folders: prompt/user/<task>.md/*.md (per scenario)
TASK_TYPE_PARAMS = {
    "forgeryscope": {
        "task_name": "forgeryscope",
        "sys_prompt_template_path": SYS_FSD,
        # NOTE: directory path; the runner should select a file within.
        "user_prompt_template_path": USR_FSD,
        "input_json_paths": [
            "./assets/dataset/image_inference_forgery.json",
            "./assets/dataset/real.json",
            "./assets/dataset/targeted_region_restoration.json",
            "./assets/dataset/targeted_region_editing.json",
            "./assets/dataset/text_constraint_fabrication.json",
        ],
        "base_folder": "assets",
        "kwargs_generator": forgeryscope_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
    "visualtext": {
        "task_name": "visualtext",
        "sys_prompt_template_path": SYS_TAR,
        "user_prompt_template_path": USR_TAR,
        "input_json_paths": [
            "./assets/dataset/image_inference_forgery.json",
            "./assets/dataset/real.json",
            "./assets/dataset/targeted_region_restoration.json",
            "./assets/dataset/targeted_region_editing.json",
            "./assets/dataset/text_constraint_fabrication.json",
        ],
        "base_folder": "assets",
        "image_filter": lambda item: item.get("with_text", False),
        "kwargs_generator": visualtext_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
    "manipulation": {
        "task_name": "manipulation",
        "sys_prompt_template_path": SYS_MC,
        "user_prompt_template_path": USR_MC,
        "input_json_paths": [
            "./assets/dataset/targeted_region_restoration.json",
            "./assets/dataset/targeted_region_editing.json",
        ],
        "base_folder": "assets",
        "kwargs_generator": manipulation_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
    "pinpointing": {
        "task_name": "pinpointing",
        "sys_prompt_template_path": SYS_TP,
        "user_prompt_template_path": USR_TP,
        "input_json_paths": [
            "./assets/dataset/targeted_region_restoration.json",
            "./assets/dataset/targeted_region_editing.json",
        ],
        "base_folder": "assets",
        "kwargs_generator": pinpointing_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
}


# Reuse the same model list as basic, but keep it minimal here.
TASK_LIST = [
    {
        "namespace": "openai/gpt-5-pro",
        "inference_func": {
            "forgeryscope": lazy_inference(
                create_openrouter_inference,
                task_type_name="Forgeryscope",
                model="openai/gpt-5-pro",
            ),
            "visualtext": lazy_inference(
                create_openrouter_inference,
                task_type_name="Visualtext",
                model="openai/gpt-5-pro",
            ),
            "manipulation": lazy_inference(
                create_openrouter_inference,
                task_type_name="Manipulation",
                model="openai/gpt-5-pro",
            ),
            "pinpointing": lazy_inference(
                create_openrouter_inference,
                task_type_name="Pinpointing",
                model="openai/gpt-5-pro",
            ),
        },
        "sample_rate": 0.1,
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
    }
]

