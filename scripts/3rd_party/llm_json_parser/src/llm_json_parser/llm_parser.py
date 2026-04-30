"""
LLM JSON parser.

This module provides a robust JSON parser for extracting valid JSON objects/arrays
from typical LLM outputs:
- wrapped in code fences (```json ... ```)
- surrounded by extra prose before/after JSON
- minor truncation/noise
"""

from __future__ import annotations

import json
import re
from typing import Union


JsonValue = Union[dict, list]


class LLMJSONParser:
    """Parse JSON from imperfect LLM outputs."""

    @staticmethod
    def parse(text: str) -> JsonValue:
        if text is None or not str(text).strip():
            raise ValueError("Empty input text.")

        raw = str(text).strip()

        # 1) Direct parse
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # 2) Strip fenced blocks: ```json ... ``` or ``` ... ```
        fenced = _strip_code_fences(raw)
        try:
            return json.loads(fenced)
        except json.JSONDecodeError:
            pass

        # 3) Extract first JSON object/array and parse
        extracted = _extract_first_json(fenced)
        try:
            return json.loads(extracted)
        except json.JSONDecodeError:
            pass

        # 4) Best-effort repair then parse
        fixed = _fix_common_issues(extracted)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON: {e}. Raw prefix: {raw[:200]!r}"
            ) from e


def parse_llm_json(text: str) -> JsonValue:
    """Convenience wrapper."""

    return LLMJSONParser.parse(text)


def _strip_code_fences(text: str) -> str:
    t = text.strip()
    if not t.startswith("```"):
        return t
    # Match a full fenced block if possible
    m = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", t, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Otherwise remove the first fence line
    nl = t.find("\n")
    if nl != -1:
        t = t[nl + 1 :].lstrip()
    # Remove trailing fence if present
    end = t.rfind("```")
    if end != -1:
        t = t[:end].strip()
    return t


def _extract_first_json(text: str) -> str:
    # Find first '{' or '['
    start = -1
    opener = None
    for i, ch in enumerate(text):
        if ch == "{":
            start = i
            opener = "{"
            break
        if ch == "[":
            start = i
            opener = "["
            break

    if start == -1 or opener is None:
        return text.strip()

    closer = "}" if opener == "{" else "]"
    depth = 0
    in_string = False
    escape = False

    for j in range(start, len(text)):
        ch = text[j]
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[start : j + 1].strip()

    return text[start:].strip()


def _fix_common_issues(text: str) -> str:
    t = text.strip()
    if not t:
        return t

    # Remove trailing commas before closing braces/brackets
    t = re.sub(r",(\s*[}\]])", r"\1", t)

    # If it looks like a JSON object missing leading '{', add it
    if t.startswith('"') and re.match(r'^\s*"[^"]+"\s*:', t):
        t = "{" + t

    # Balance braces/brackets in a simple way
    opens = {"{": "}", "[": "]"}
    stack = []
    in_string = False
    escape = False
    for ch in t:
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch in opens:
            stack.append(opens[ch])
        elif stack and ch == stack[-1]:
            stack.pop()

    return t + "".join(reversed(stack))

