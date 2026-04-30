from __future__ import annotations

from typing import Dict

from .utils import (
    get_caption_from_path,
    get_vec_query,
    image2base64,
    infer_answer_from_path,
    infer_dataset_category_from_path,
    random_generate_question,
)


def manipulation_kwargs_generator(
    base_folder="assets", dataset_folder="assets", highlight_folder="assets"
):
    """
    Build kwargs for few-shot manipulation classification.
    """

    choose = ["A", "B", "C", "D"]
    content = ["Remove", "Insert", "Alter", "Unknown"]

    def image_kwargs(image_path) -> Dict:
        vec_query = get_vec_query()
        paths = vec_query.query(
            image2base64(image_path),
            dataset_category=infer_dataset_category_from_path(image_path),
        )
        ref_image_path = paths[0].get("image_path")
        pair_dict, shuffle_question = random_generate_question(content, choose)
        return {
            "images": [
                image2base64(
                    highlight_folder + "/" + ref_image_path.replace("fake", "highlight")
                ),
                image2base64(image_path.replace("fake", "highlight")),
            ],
            "option_block": shuffle_question,
            "type_ref": infer_answer_from_path(
                ref_image_path,
                f"{base_folder}/reference_answer/manipulation_classification.json",
            ),
            "reference_caption": paths[0].get("original_caption"),
            "test_caption": get_caption_from_path(
                image_path,
                [
                    f"{dataset_folder}/dataset/targeted_region_restoration.json",
                    f"{dataset_folder}/dataset/targeted_region_editing.json",
                ],
            ),
            "record_params": {
                "images": [
                    highlight_folder + "/" + ref_image_path.replace("fake", "highlight"),
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

