from __future__ import annotations

import os
from typing import Dict

from .utils import (
    get_vec_query,
    image2base64,
    infer_answer_from_path,
    infer_dataset_category_from_path,
    random_generate_question,
)


def forgeryscope_kwargs_generator(base_folder="assets", dataset_folder="assets"):
    """
    Build kwargs for few-shot forgery scope discrimination.

    The returned kwargs include two images:
    1) a retrieved reference image (authentic baseline)
    2) the test image
    """

    choose = ["A", "B", "C", "D"]
    content = ["Entire Forgery", "Partial Forgery", "Not sure", "No Forgery"]

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
                image2base64(os.path.join(dataset_folder, ref_image_path)),
                image2base64(image_path),
            ],
            "option_block": shuffle_question,
            "type_ref": infer_answer_from_path(
                ref_image_path,
                f"{base_folder}/reference_answer/forgery_scope_discrimination.json",
            ),
            "record_params": {
                "images": [dataset_folder + "/" + ref_image_path, image_path],
                "question": pair_dict,
                "correct_answer": pair_dict.get(
                    infer_answer_from_path(
                        image_path,
                        f"{base_folder}/reference_answer/forgery_scope_discrimination.json",
                    )
                ),
            },
        }

    return image_kwargs

