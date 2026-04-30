from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Literal, Optional

from llm_json_parser import parse_llm_json


def create_ali_inference(
    task_type_name: Literal["Forgeryscope", "Manipulation", "Visualtext", "Any"],
    model: str = "ali/qwen3-vl-plus",
    thinking: bool = False,
    json_schema_limit: bool = False,
    api_key: Optional[str] = os.environ.get("ALI_API_KEY"),
    base_url: Optional[str] = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature: float = 0.7,
) -> Callable:
    """
    Create an Ali (DashScope-compatible) inference function.
    """

    try:
        from openai import OpenAI
    except ImportError as e:
        raise ImportError('Please install the "openai" package: pip install openai') from e

    from . import pydantic_defination

    try:
        model_class = getattr(pydantic_defination, task_type_name)
    except AttributeError as e:
        raise ValueError(f"Response schema not found for task type: {task_type_name}") from e

    extra_body = {"thinking": {"type": "enabled" if thinking else "disabled"}}

    if json_schema_limit:
        response_format = {
            "type": "json_schema",
            "name": model_class.__name__,
            "schema": model_class.model_json_schema(),
            "strict": True,
        }
    else:
        response_format = {"type": "json_object"}

    model_name = model.split("/")[-1]

    client_kwargs: Dict[str, Any] = {}
    if api_key is not None:
        client_kwargs["api_key"] = api_key
    if base_url is not None:
        client_kwargs["base_url"] = base_url
    client = OpenAI(**client_kwargs)

    def inference_func(messages: List[Dict]) -> Any:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            response_format=response_format,
            extra_body=extra_body,
        )
        return parse_llm_json(response.choices[0].message.content)

    return inference_func

