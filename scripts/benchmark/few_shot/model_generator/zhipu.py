from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Literal, Optional

from llm_json_parser import parse_llm_json


def create_zhipu_inference(
    task_type_name: Literal["Forgeryscope", "Manipulation", "Visualtext", "Any"],
    model: str = "zhipu/glm-4.1v-thinking-flash",
    thinking: bool = False,
    api_key: Optional[str] = os.environ.get("ZHIPU_API_KEY"),
    base_url: Optional[str] = "https://open.bigmodel.cn/api/paas/v4",
    temperature: float = 0.7,
) -> Callable:
    """
    Create a Zhipu inference function (OpenAI-compatible client).
    """

    try:
        from openai import OpenAI
    except ImportError as e:
        raise ImportError('Please install the "openai" package: pip install openai') from e

    extra_body = {"thinking": {"type": "enabled" if thinking else "disabled"}}
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

