def random_generate_question(content, choose):
    import random

    # Create an independent RNG instance
    local_random = random.Random()
    local_random.shuffle(content)
    paired = list(zip(content, choose))
    pair_dict = dict(paired)
    options_block = "\n".join([f"{letter}. {text}" for text, letter in paired])
    return pair_dict, options_block


def image2base64(file_path):
    import base64
    from PIL import Image

    with Image.open(file_path) as img:
        # PIL validates the image when opening it
        img_format = (img.format or "").lower()
        mime_type = f"image/{img_format if img_format != 'jpeg' else 'jpeg'}"

    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"


def infer_dataset_category_from_path(path: str) -> str:
    search_index = {
        "image_inference_forgery": "image_inference_forgery",
        "real": "real",
        "targeted_region_editing": "targeted_region_editing",
        "targeted_region_restoration": "targeted_region_restoration",
        "text_constraint_fabrication": "text_constraint_fabrication",
    }
    for key, value in search_index.items():
        if key in path:
            return value
    print(f"\nError finding category: {path}")
    exit(1)


import json


def infer_answer_from_path(path: str, answer_json_path: str) -> str:
    search_index = {}
    with open(answer_json_path, "r") as f:
        search_index = json.load(f)
    for key, value in search_index.items():
        if (key in path) or (key == path):
            return value
    print(f"\nError finding {path} answer in:\n {answer_json_path}")
    exit(1)


from typing import List


def get_caption_from_path(path: str, search_json_paths: List[str]) -> str:
    search_index = {}
    for search_json_path in search_json_paths:
        with open(search_json_path, "r") as f:
            search_index = json.load(f)
            for item in search_index:
                if item.get("image_path") in path:
                    return item["original_caption"]
    print(f"\nError finding caption: {path}")
    exit(1)
