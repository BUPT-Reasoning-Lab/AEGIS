import os
from PIL import Image, ImageFilter


class GaussianBlur:
    """Gaussian blur processor."""

    def __init__(self, radius=5, verbose=True):
        """
        Initialize the gaussian blur processor.

        Args:
            radius: Blur radius; higher means stronger blur (default: 5).
            verbose: Whether to print progress logs (default: True).
        """
        self.radius = radius
        self.verbose = verbose

    def process_image(self, input_path, output_path):
        """
        Apply gaussian blur to a single image.

        Args:
            input_path: Input image path.
            output_path: Output image path.
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Open image and apply gaussian blur
        img = Image.open(input_path)
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        blurred_img.save(output_path)

        if self.verbose:
            print(f"Processed: {input_path} -> {output_path}")
