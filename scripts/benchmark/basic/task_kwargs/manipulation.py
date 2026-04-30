from typing import Dict

from .utils import (
    image2base64,
    infer_answer_from_path,
    random_generate_question,
    get_caption_from_path,
)


def manipulation_kwargs_generator(dataset_folder="assets", base_folder="assets"):
    """
    Generate function kwargs for image inference task.
    args:
        dataset_folder: str, the base folder of the dataset folder.
        base_folder: str, the base folder of the reference_answer folder.
    """
    choose = ["A", "B", "C", "D"]
    content = ["Remove", "Insert", "Alter", "Unknown"]

    def image_kwargs(image_path) -> Dict:
        pair_dict, shuffle_question = random_generate_question(content, choose)
        return {
            "images": [
                image2base64(image_path.replace("fake", "highlight")),
            ],
            "OPTIONS_BLOCK": shuffle_question,
            "CAPTION_TEXT": get_caption_from_path(
                image_path,
                [
                    f"{dataset_folder}/dataset/targeted_region_restoration.json",
                    f"{dataset_folder}/dataset/targeted_region_editing.json",
                ],
            ),
            "record_params": {
                "images": [
                    image_path.replace("fake", "highlight"),
                ],
                "question": pair_dict,
                "correct_answer": pair_dict.get(
                    infer_answer_from_path(
                        image_path,
                        f"{base_folder}/reference_answer/manipulation_classification.json",
                    )
                ),
            },
        }

    return image_kwargs
