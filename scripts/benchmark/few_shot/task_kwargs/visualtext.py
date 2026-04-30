from __future__ import annotations

from typing import Dict

from .utils import (
    get_vec_query,
    image2base64,
    infer_answer_from_path,
    infer_dataset_category_from_path,
    random_generate_question,
)


def visualtext_kwargs_generator(base_folder="assets", dataset_folder="assets"):
    """
    Build kwargs for few-shot textual artifact recognition.
    """

    choose = ["A", "B"]
    content = ["Yes", "No"]

    STR_YES = (
        "contains some AI-generated or AI-edited text forgeries or semantic mismatches "
        "between the embedded text and the scientific content"
    )
    STR_NO = "is real"
    STR_TEMPLATE_DICT = {"Yes": STR_YES, "No": STR_NO}

    def image_kwargs(image_path) -> Dict:
        vec_query = get_vec_query()
        paths = vec_query.query(
            image2base64(image_path),
            dataset_category=infer_dataset_category_from_path(image_path),
            with_text=True,
        )
        ref_image_path = paths[0].get("image_path")
        pair_dict, shuffle_question = random_generate_question(content, choose)
        return {
            "images": [
                image2base64(dataset_folder + "/" + ref_image_path),
                image2base64(image_path),
            ],
            "option_block": shuffle_question,
            "type_ref": STR_TEMPLATE_DICT.get(
                infer_answer_from_path(
                    ref_image_path,
                    f"{base_folder}/reference_answer/textual_artifact_recognition.json",
                )
            ),
            "record_params": {
                "images": [dataset_folder + "/" + ref_image_path, image_path],
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

