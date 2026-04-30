import os
from PIL import Image


class ScaleImage:
    """Image scaling processor."""

    def __init__(self, scale_factor=0.5, resample_method="LANCZOS", verbose=True):
        """
        Initialize the image scaling processor.

        Args:
            scale_factor: Scale factor relative to original size (default: 0.5).
            resample_method: Resampling method: 'LANCZOS', 'BILINEAR', 'BICUBIC', or 'NEAREST' (default: 'LANCZOS').
            verbose: Whether to print progress logs (default: True).
        """
        self.scale_factor = scale_factor
        self.resample_method = resample_method
        self.verbose = verbose

    def _get_resample_method(self):
        """
        Get the PIL resampling method constant.

        Returns:
            A PIL resampling method constant.
        """
        methods = {
            "LANCZOS": Image.LANCZOS,
            "BILINEAR": Image.BILINEAR,
            "BICUBIC": Image.BICUBIC,
            "NEAREST": Image.NEAREST,
        }
        return methods.get(self.resample_method, Image.LANCZOS)

    def process_image(self, input_path, output_path):
        """
        Scale a single image.

        Args:
            input_path: Input image path.
            output_path: Output image path.
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Open image and scale
        img = Image.open(input_path)
        new_width = int(img.width * self.scale_factor)
        new_height = int(img.height * self.scale_factor)

        # Use the specified resampling method
        resample = self._get_resample_method()
        scaled_img = img.resize((new_width, new_height), resample)
        scaled_img.save(output_path)

        if self.verbose:
            print(f"Processed: {input_path} -> {output_path}")
            print(f"  Size: {img.width}x{img.height} -> {new_width}x{new_height}")
