from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Literal, Optional

from llm_json_parser import parse_llm_json


def create_bytedance_inference(
    task_type_name: Literal["Forgeryscope", "Manipulation", "Visualtext", "Any"],
    model: str = "bytedance/doubao-seed-1-6",
    thinking: bool = False,
    json_limit: Literal["Strict", "Loose", "None"] = "Strict",
    api_key: Optional[str] = os.environ.get("BYTE_API_KEY"),
    base_url: Optional[str] = "https://ark.cn-beijing.volces.com/api/v3",
    temperature: float = 0.7,
) -> Callable:
    """
    Create a ByteDance (Volc Ark) inference function (OpenAI-compatible client).
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

    if json_limit == "Loose":
        response_format = {"type": "json_object"}
    elif json_limit == "Strict":
        response_format = {
            "type": "json_schema",
            "name": model_class.__name__,
            "schema": model_class.model_json_schema(),
            "strict": True,
        }
    else:
        response_format = None

    model_name = model.split("/")[-1]

    client_kwargs: Dict[str, Any] = {}
    if api_key is not None:
        client_kwargs["api_key"] = api_key
    if base_url is not None:
        client_kwargs["base_url"] = base_url
    client = OpenAI(**client_kwargs)

    def inference_func(messages: List[Dict]) -> Any:
        if response_format is not None:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                response_format=response_format,
                extra_body=extra_body,
            )
        else:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                extra_body=extra_body,
            )
        return parse_llm_json(response.choices[0].message.content)

    return inference_func

