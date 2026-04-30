from .gauss_blur import GaussianBlur
from .jpeg_compress import JpegCompress
from .scale_image import ScaleImage

__all__ = ["GaussianBlur", "JpegCompress", "ScaleImage"]

import importlib.metadata

metadata = importlib.metadata.metadata(__package__ or __name__)

__version__ = metadata["Version"]
__author__ = metadata["Author"]
