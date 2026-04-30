"""
LLM JSON Parser - A robust JSON parser for extracting JSON from LLM outputs.
"""

from .llm_parser import LLMJSONParser, parse_llm_json

__all__ = ["LLMJSONParser", "parse_llm_json"]

import importlib.metadata

try:
    _metadata = importlib.metadata.metadata(__package__ or __name__)
    __version__ = _metadata.get("Version", "0.0.0")
    __author__ = _metadata.get("Author", "")
except importlib.metadata.PackageNotFoundError:
    # When imported from source (vendored), dist metadata may be unavailable.
    __version__ = "0.0.0"
    __author__ = ""
