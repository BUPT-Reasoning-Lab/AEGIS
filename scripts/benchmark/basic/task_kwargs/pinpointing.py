from typing import Dict

from .utils import (
    image2base64,
    infer_answer_from_path,
)


def pinpointing_kwargs_generator(base_folder="assets"):
    """
    Generate function kwargs for image inference task.
    args:
        base_folder: str, the base folder of the reference_answer folder.
    """

    def image_kwargs(image_path) -> Dict:
        from PIL import Image

        width, height = Image.open(image_path).size
        return {
            "images": [
                image2base64(image_path),
            ],
            "WIDTH": width,
            "HEIGHT": height,
            "MIN_AREA": int(width * height * 0.02),
            "MAX_AREA": int(width * height * 0.40),
            "WIDTH_1": width - 1,
            "HEIGHT_1": height - 1,
            "record_params": {
                "images": [image_path],
                "image_size": {
                    "width": width,
                    "height": height,
                },
                "correct_answer": infer_answer_from_path(
                    image_path,
                    f"{base_folder}/reference_answer/tampering_pinpointing.json",
                ),
            },
        }

    return image_kwargs
