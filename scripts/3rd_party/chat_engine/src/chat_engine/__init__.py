from .processor_builder import Processor

__all__ = [
    "Processor",
]
import importlib.metadata

metadata = importlib.metadata.metadata(__package__ or __name__)

__version__ = metadata["Version"]
__author__ = metadata["Author"]
