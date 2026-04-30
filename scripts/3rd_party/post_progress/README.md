# post_progress

Lightweight image post-processing utilities for common degradations/compression.
This package provides three processors:

- `GaussianBlur`: gaussian blur
- `JpegCompress`: JPEG compression (with RGBA -> RGB conversion)
- `ScaleImage`: image scaling (multiple resampling methods)

They are designed to be easy to integrate into scripts or data pipelines. Each
processor saves results to disk and optionally prints progress logs when
`verbose=True`.

Exports
```post_progress/src/post_progress/__init__.py#L1-50
from .gauss_blur import GaussianBlur
from .jpeg_compress import JpegCompress
from .scale_image import ScaleImage

__all__ = ["GaussianBlur", "JpegCompress", "ScaleImage"]

```

Quick start

1. Install dependencies (recommended in a virtual environment):

```/dev/null/example-install.sh#L1-10
uv add /path/to/whl.whl
```

2. Use in a script (minimal example):

```/dev/null/usage_example.py#L1-200
from post_progress import GaussianBlur, JpegCompress, ScaleImage

# Gaussian blur
gb = GaussianBlur(radius=3, verbose=True)
gb.process_image("data/input.jpg", "out/blurred.jpg")

# JPEG compression
jc = JpegCompress(quality=30, verbose=True)
jc.process_image("data/input.png", "out/compressed.jpg")

# Scaling
si = ScaleImage(scale_factor=0.5, resample_method="LANCZOS", verbose=True)
si.process_image("data/input.jpg", "out/scaled.jpg")
```

API

- GaussianBlur
  - File: `post_progress/src/post_progress/gauss_blur.py`
  - Init:
    - `GaussianBlur(radius=5, verbose=True)`
      - `radius`: blur radius (default: 5)
      - `verbose`: print logs (default: True)
  - Method:
    - `process_image(input_path, output_path)`: apply gaussian blur and save to `output_path` (creates output directory).

Reference implementation:
```post_progress/src/post_progress/gauss_blur.py#L1-200
import os
from PIL import Image, ImageFilter

class GaussianBlur:
    """Gaussian blur processor."""

    def __init__(self, radius=5, verbose=True):
        ...
    def process_image(self, input_path, output_path):
        ...
```

- JpegCompress
  - File: `post_progress/src/post_progress/jpeg_compress.py`
  - Init:
    - `JpegCompress(quality=50, verbose=True)`
      - `quality`: JPEG quality, 1-100 (lower => stronger compression, default: 50)
      - `verbose`: print logs
  - Method:
    - `process_image(input_path, output_path)`: save as JPEG with `quality` (RGBA inputs are converted to RGB). Returns the actual output path (forced `.jpg`).

Reference implementation:
```post_progress/src/post_progress/jpeg_compress.py#L1-200
import os
from PIL import Image

class JpegCompress:
    """JPEG compression processor."""

    def __init__(self, quality=50, verbose=True):
        ...
    def process_image(self, input_path, output_path):
        ...
```

- ScaleImage
  - File: `post_progress/src/post_progress/scale_image.py`
  - Init:
    - `ScaleImage(scale_factor=0.5, resample_method="LANCZOS", verbose=True)`
      - `scale_factor`: scale factor (e.g., 0.5 => 50%)
      - `resample_method`: `"LANCZOS"`, `"BILINEAR"`, `"BICUBIC"`, `"NEAREST"`
      - `verbose`: print logs
  - Method:
    - `process_image(input_path, output_path)`: scale and save to `output_path`.

Reference implementation:
```post_progress/src/post_progress/scale_image.py#L1-200
import os
from PIL import Image

class ScaleImage:
    """Image scaling processor."""

    def __init__(self, scale_factor=0.5, resample_method="LANCZOS", verbose=True):
        ...
    def process_image(self, input_path, output_path):
        ...
```

Tips & notes

- Input/output
  - `process_image` accepts any Pillow-supported format and creates output dirs automatically.
  - `JpegCompress` forces `.jpg` outputs and converts RGBA -> RGB for JPEG compatibility.

- Performance
  - These processors run synchronously per image; use `concurrent.futures` in your caller for parallel processing.

- Resampling
  - Use `LANCZOS` for high-quality scaling. `NEAREST` is fastest but lowest quality.

- Error handling
  - Exceptions are not universally caught; callers should handle errors as needed.

Example: batch process images with a chain (scale -> blur -> JPEG compress)
```/dev/null/chain_example.py#L1-200
from pathlib import Path
from post_progress import ScaleImage, GaussianBlur, JpegCompress

src_dir = Path("dataset/images")
out_dir = Path("dataset/processed")
out_dir.mkdir(parents=True, exist_ok=True)

scale = ScaleImage(scale_factor=0.6, resample_method="LANCZOS", verbose=False)
blur = GaussianBlur(radius=2, verbose=False)
compress = JpegCompress(quality=40, verbose=True)

for p in src_dir.glob("*.*"):
    scaled_path = out_dir / f"{p.stem}_scaled{p.suffix}"
    scale.process_image(str(p), str(scaled_path))

    blurred_path = out_dir / f"{p.stem}_scaled_blur{p.suffix}"
    blur.process_image(str(scaled_path), str(blurred_path))

    final_path = out_dir / f"{p.stem}_final.jpg"
    compress.process_image(str(blurred_path), str(final_path))
```
