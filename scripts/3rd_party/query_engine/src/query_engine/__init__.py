from .query import VecQuery
from .embedder import Embedder

__all__ = [
    "VecQuery",
    "Embedder",
]

import importlib.metadata

metadata = importlib.metadata.metadata(__package__ or __name__)

__version__ = metadata["Version"]
__author__ = metadata["Author"]
