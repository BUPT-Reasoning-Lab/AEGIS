from __future__ import annotations

from .model_generator import *
from .prompt import *
from .task_kwargs import *


RANDOM_SEED = 42
OUTPUT_FOLDER = "results_few_shot"


def lazy_inference(factory, /, **factory_kwargs):
    """Defer inference client creation until the first call."""

    _fn = None

    def _call(messages):
        nonlocal _fn
        if _fn is None:
            _fn = factory(**factory_kwargs)
        return _fn(messages)

    return _call


TASK_TYPE_PARAMS = {
    "forgeryscope": {
        "task_name": "forgeryscope",
        "sys_prompt_template_path": SYS_FORGERYSCOPE,
        "user_prompt_template_path": USR_FORGERYSCOPE,
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
        "sys_prompt_template_path": SYS_VISUALTEXT,
        "user_prompt_template_path": USR_VISUALTEXT,
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
        "sys_prompt_template_path": SYS_MANIPULATION,
        "user_prompt_template_path": USR_MANIPULATION,
        "input_json_paths": [
            "./assets/dataset/targeted_region_restoration.json",
            "./assets/dataset/targeted_region_editing.json",
        ],
        "base_folder": "assets",
        "kwargs_generator": manipulation_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
}


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
        },
        "sample_rate": 0.1,
        "task_list": ["forgeryscope", "visualtext", "manipulation"],
    },
    {
        "namespace": "zhipu/glm-4.1v-thinking-flash",
        "inference_func": lazy_inference(
            create_zhipu_inference,
            task_type_name="Any",
            model="zhipu/glm-4.1v-thinking-flash",
        ),
        "sample_rate": {
            "forgeryscope": 0.002,
            "visualtext": 0.01,
            "manipulation": 0.01,
        },
        "task_list": ["forgeryscope", "visualtext", "manipulation"],
    },
    {
        "namespace": "ali/qwen3-vl-plus",
        "inference_func": {
            "forgeryscope": lazy_inference(
                create_ali_inference,
                task_type_name="Forgeryscope",
                model="ali/qwen3-vl-plus",
            ),
            "manipulation": lazy_inference(
                create_ali_inference,
                task_type_name="Manipulation",
                model="ali/qwen3-vl-plus",
            ),
            "visualtext": lazy_inference(
                create_ali_inference,
                task_type_name="Visualtext",
                model="ali/qwen3-vl-plus",
            ),
        },
        "task_list": ["forgeryscope", "visualtext", "manipulation"],
    },
]

