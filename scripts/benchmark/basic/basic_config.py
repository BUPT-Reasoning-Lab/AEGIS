from .model_generator import *
from .prompt import *
from .task_kwargs import *


# Make sure all models do the same question
RANDOM_SEED = 42
OUTPUT_FOLDER = "results"


def lazy_inference(factory, /, **factory_kwargs):
    """
    Defer inference client creation until the first call.

    This keeps `basic_config` importable even when optional runtime dependencies
    (e.g., `openai`, `Pillow`) are not installed in the current environment.
    """

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
    "pinpointing": {
        "task_name": "pinpointing",
        "sys_prompt_template_path": SYS_PINPOINTING,
        "user_prompt_template_path": USR_PINPOINTING,
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


TASK_LIST = [
    ###################################### Demo code
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
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
    },
    ###################################### End Demo code
    # ---- work line ----
    # Close Model
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
            "pinpointing": lazy_inference(
                create_ali_inference,
                task_type_name="Pinpointing",
                model="ali/qwen3-vl-plus",
            ),
            "visualtext": lazy_inference(
                create_ali_inference,
                task_type_name="Visualtext",
                model="ali/qwen3-vl-plus",
            ),
        },
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
    },
    {
        "namespace": "google/gemini-3-pro-preview",
        "inference_func": {
            "forgeryscope": lazy_inference(
                create_openrouter_inference,
                task_type_name="Forgeryscope",
                model="google/gemini-3-pro-preview",
            ),
            "visualtext": lazy_inference(
                create_openrouter_inference,
                task_type_name="Visualtext",
                model="google/gemini-3-pro-preview",
            ),
            "manipulation": lazy_inference(
                create_openrouter_inference,
                task_type_name="Manipulation",
                model="google/gemini-3-pro-preview",
            ),
            "pinpointing": lazy_inference(
                create_openrouter_inference,
                task_type_name="Pinpointing",
                model="google/gemini-3-pro-preview",
            ),
        },
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
    },
    {
        "namespace": "anthropic/claude-sonnet-4.5",
        "inference_func": {
            "forgeryscope": lazy_inference(
                create_openrouter_inference,
                task_type_name="Forgeryscope",
                model="anthropic/claude-sonnet-4.5",
            ),
            "visualtext": lazy_inference(
                create_openrouter_inference,
                task_type_name="Visualtext",
                model="anthropic/claude-sonnet-4.5",
            ),
            "manipulation": lazy_inference(
                create_openrouter_inference,
                task_type_name="Manipulation",
                model="anthropic/claude-sonnet-4.5",
            ),
            "pinpointing": lazy_inference(
                create_openrouter_inference,
                task_type_name="Pinpointing",
                model="anthropic/claude-sonnet-4.5",
            ),
        },
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
        "sample_rate": 0.1,
    },
    {
        "namespace": "openai/gpt-5.1",
        "inference_func": {
            "forgeryscope": lazy_inference(
                create_openrouter_inference,
                task_type_name="Forgeryscope",
                model="openai/gpt-5.1",
            ),
            "visualtext": lazy_inference(
                create_openrouter_inference,
                task_type_name="Visualtext",
                model="openai/gpt-5.1",
            ),
            "manipulation": lazy_inference(
                create_openrouter_inference,
                task_type_name="Manipulation",
                model="openai/gpt-5.1",
            ),
            "pinpointing": lazy_inference(
                create_openrouter_inference,
                task_type_name="Pinpointing",
                model="openai/gpt-5.1",
            ),
        },
        "sample_rate": 0.1,
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
    },
    # Opensource Model
    {
        "namespace": "meta-llama/llama-4-maverick",
        "inference_func": {
            "forgeryscope": lazy_inference(
                create_openrouter_inference,
                task_type_name="Forgeryscope",
                model="meta-llama/llama-4-maverick",
            ),
            "visualtext": lazy_inference(
                create_openrouter_inference,
                task_type_name="Visualtext",
                model="meta-llama/llama-4-maverick",
            ),
            "manipulation": lazy_inference(
                create_openrouter_inference,
                task_type_name="Manipulation",
                model="meta-llama/llama-4-maverick",
            ),
            "pinpointing": lazy_inference(
                create_openrouter_inference,
                task_type_name="Pinpointing",
                model="meta-llama/llama-4-maverick",
            ),
        },
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
    },
    {
        "namespace": "mistralai/ministral-14b-2512",
        "inference_func": {
            "forgeryscope": lazy_inference(
                create_openrouter_inference,
                task_type_name="Forgeryscope",
                model="mistralai/ministral-14b-2512",
            ),
            "visualtext": lazy_inference(
                create_openrouter_inference,
                task_type_name="Visualtext",
                model="mistralai/ministral-14b-2512",
            ),
            "manipulation": lazy_inference(
                create_openrouter_inference,
                task_type_name="Manipulation",
                model="mistralai/ministral-14b-2512",
            ),
            "pinpointing": lazy_inference(
                create_openrouter_inference,
                task_type_name="Pinpointing",
                model="mistralai/ministral-14b-2512",
            ),
        },
        "task_list": ["forgeryscope", "visualtext", "manipulation", "pinpointing"],
    },
    # ---- working line ----
]
