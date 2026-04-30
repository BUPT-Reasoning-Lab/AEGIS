from llm_json_parser import parse_llm_json
from typing import Callable, Any, List, Dict, Optional, Literal
import os


def create_bytedance_inference(
    task_type_name: Literal[
        "Forgeryscope", "Manipulation", "Visualtext", "Pinpointing", "Any"
    ],
    model: str = "bytedance/doubao-seed-1-6",
    thinking: bool = False,
    json_limit: Literal["Strict", "Loose", "None"] = "Strict",
    api_key: Optional[str] = os.environ.get("BYTE_API_KEY"),
    base_url: Optional[str] = "https://ark.cn-beijing.volces.com/api/v3",
    temperature: float = 0.7,
) -> Callable:
    """
    Create a ByteDance (Volc Ark) inference function (OpenAI-compatible client).

    Args:
        task_type_name: Task type name: "Forgeryscope", "Manipulation", "Visualtext", "Pinpointing", or "Any".
        model: Model name. Default: "bytedance/doubao-seed-1-6".
        thinking: Whether to enable the provider's "thinking" mode.
        json_limit: "Strict" (JSON schema), "Loose" (JSON object), or "None" (no enforced format).
        api_key: API key. Default: read from the "BYTE_API_KEY" environment variable.
        base_url: Base URL. Default: Beijing endpoint.
        temperature: Sampling temperature.

    Returns:
        A callable that takes OpenAI-style `messages` and returns a parsed JSON object.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError('Please install the "openai" package: pip install openai')
    # Dynamically load the response schema
    from . import pydantic_defination

    try:
        model_class = getattr(pydantic_defination, task_type_name)
    except AttributeError:
        raise ValueError(f"Response schema not found for task type: {task_type_name}")

    # Thinking control
    if thinking:
        extra_body = {"thinking": {"type": "enabled"}}
    else:
        extra_body = {"thinking": {"type": "disabled"}}

    # JSON output format control
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

    # Provider model id
    model_name = model.split("/")[-1]

    # Client init
    client_kwargs = {}
    if api_key is not None:
        client_kwargs["api_key"] = api_key
    if base_url is not None:
        client_kwargs["base_url"] = base_url
    client = OpenAI(**client_kwargs)

    def inference_func(messages: List[Dict]) -> Any:
        """
        Call the chat completion API.

        Args:
            messages: Message list in OpenAI chat format.
            [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

        Returns:
            Parsed JSON result.
        """
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
