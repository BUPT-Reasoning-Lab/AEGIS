from typing import Dict


from .utils import (
    image2base64,
    infer_answer_from_path,
    random_generate_question,
)


def visualtext_kwargs_generator(base_folder="assets"):
    """
    Generate function kwargs for image inference task.
    args:
        base_folder: str, the base folder of the reference_answer folder.
    """

    choose = ["A", "B"]
    content = ["Yes", "No"]

    def image_kwargs(image_path) -> Dict:
        pair_dict, shuffle_question = random_generate_question(content, choose)
        return {
            "images": [
                image2base64(image_path),
            ],
            "OPTIONS_BLOCK": shuffle_question,
            "record_params": {
                "images": [image_path],
                "question": pair_dict,
                "correct_answer": pair_dict.get(
                    infer_answer_from_path(
                        image_path,
                        f"{base_folder}/reference_answer/textual_artifact_recognition.json",
                    )
                ),
            },
        }

    return image_kwargs
