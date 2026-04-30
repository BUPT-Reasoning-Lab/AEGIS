import torch
from transformers import AutoImageProcessor, AutoModel
from transformers.image_utils import load_image


class Embedder:
    def __init__(self, model_name_or_path):
        self.processor = AutoImageProcessor.from_pretrained(model_name_or_path)
        self.model = AutoModel.from_pretrained(
            model_name_or_path,
            dtype=torch.float16,
            device_map="auto",
            attn_implementation="sdpa",
        )
        print("Embedder Initialized.")

    def embed(self, image_path):
        image = load_image(image_path)
        inputs = self.processor(images=image, return_tensors="pt").to(self.model.device)
        with torch.inference_mode():
            outputs = self.model(**inputs)
        pooled_output = outputs.pooler_output
        return pooled_output
