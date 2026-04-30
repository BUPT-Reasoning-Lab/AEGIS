import os
from PIL import Image


class JpegCompress:
    """JPEG compression processor."""

    def __init__(self, quality=50, verbose=True):
        """
        Initialize the JPEG compression processor.

        Args:
            quality: JPEG quality (1-100). Lower means stronger compression (default: 50).
            verbose: Whether to print progress logs (default: True).
        """
        self.quality = quality
        self.verbose = verbose

    def process_image(self, input_path, output_path):
        """
        Apply JPEG compression to a single image.

        Args:
            input_path: Input image path.
            output_path: Output image path.

        Returns:
            The actual output path (may be changed to a .jpg suffix).
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Open image and apply JPEG compression
        img = Image.open(input_path)

        # Convert RGBA to RGB for JPEG
        if img.mode == "RGBA":
            img = img.convert("RGB")

        # Ensure output path uses a .jpg suffix
        output_path_jpg = os.path.splitext(output_path)[0] + ".jpg"

        img.save(output_path_jpg, "JPEG", quality=self.quality)

        if self.verbose:
            print(f"Processed: {input_path} -> {output_path_jpg}")

        return output_path_jpg
