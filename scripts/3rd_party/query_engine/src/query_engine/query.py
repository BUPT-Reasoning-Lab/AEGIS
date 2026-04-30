import sqlite3
import json
import base64
import io
import numpy as np
from PIL import Image
from typing import List, Dict, Optional

# import torch
from .embedder import Embedder


def _base64_to_image(base64_str: str) -> str:
    """
    Convert a base64 string into a temporary image file.

    Args:
        base64_str: Base64-encoded image string (data URL supported).

    Returns:
        Path to the temporary image file.
    """
    # Strip data URI prefix if present
    if "," in base64_str:
        base64_str = base64_str.split(",", 1)[1]

    # Decode base64
    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data))

    # Save to a temporary file
    temp_path = "/tmp/query_image.png"
    image.save(temp_path)

    return temp_path


def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        vec1: First vector.
        vec2: Second vector.

    Returns:
        Cosine similarity (higher is more similar).
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    # Compute cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def _cosine_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine distance between two vectors.

    Args:
        vec1: First vector.
        vec2: Second vector.

    Returns:
        Cosine distance (lower is more similar).
    """
    return 1.0 - _cosine_similarity(vec1, vec2)


class VecQuery:
    def __init__(self, db_path: str, model_name_or_path: str):
        """
        Initialize the vector query client.

        Args:
            db_path: Path to the SQLite database file.
            model_name_or_path: Embedder model name or local path.
        """
        self.db_path = db_path
        self.embedder = Embedder(model_name_or_path)
        print("Vector Query Initialized.")

    def query(
        self,
        image_base64: str,
        category: Optional[str] = None,
        sub_type: Optional[str] = None,
        dataset_category: Optional[str] = None,
        with_text: Optional[bool] = None,
        result_size: int = 1,
    ) -> List[Dict]:
        """
        Query records most similar to a given image.

        Args:
            image_base64: Base64-encoded query image.
            category: Optional category filter.
            sub_type: Optional subtype filter.
            dataset_category: Optional dataset category filter.
            with_text: Optional with_text filter.
            result_size: Number of results to return (default: 1).

        Returns:
            A list of similar records. Each record contains all fields except
            `vector_index`, plus similarity information.
        """
        # Convert base64 into a temp image file
        temp_image_path = _base64_to_image(image_base64)

        # Generate an embedding vector for the query image
        query_embedding = self.embedder.embed(temp_image_path)
        query_vector = query_embedding.cpu().numpy().flatten().tolist()

        # Build SQL query
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # enable column-name access
        cursor = conn.cursor()

        # Build WHERE clauses
        where_clauses = ["vector_index IS NOT NULL"]
        params = []

        if category is not None:
            where_clauses.append("category = ?")
            params.append(category)

        if sub_type is not None:
            where_clauses.append("sub_type = ?")
            params.append(sub_type)

        if dataset_category is not None:
            where_clauses.append("dataset_category = ?")
            params.append(dataset_category)

        if with_text is not None:
            where_clauses.append("with_text = ?")
            params.append(int(with_text))

        where_clause = " AND ".join(where_clauses)

        # Fetch matching records
        query_sql = f"""
            SELECT id, image_name, category, sub_type, with_text,
                   image_path, generated_model, original_caption,
                   mask_path, dataset_category, vector_index
            FROM papers
            WHERE {where_clause}
        """

        cursor.execute(query_sql, params)
        records = cursor.fetchall()

        # Compute distance/similarity for each record
        similarities = []

        for record in records:
            try:
                # Parse stored vectors
                vector_json = record["vector_index"]
                db_vector = json.loads(vector_json)

                # If nested lists exist, use the first vector
                if isinstance(db_vector[0], list):
                    db_vector = db_vector[0]

                # Compute cosine distance
                distance = _cosine_distance(query_vector, db_vector)

                # Build result record (exclude vector_index)
                result_record = {
                    "id": record["id"],
                    "image_name": record["image_name"],
                    "category": record["category"],
                    "sub_type": record["sub_type"],
                    "with_text": record["with_text"],
                    "image_path": record["image_path"],
                    "generated_model": record["generated_model"],
                    "original_caption": record["original_caption"],
                    "mask_path": record["mask_path"],
                    "dataset_category": record["dataset_category"],
                    "similarity_score": 1.0
                    - distance,  # similarity score (higher is more similar)
                    "distance": distance,  # keep distance for internal sorting
                }

                similarities.append(result_record)

            except Exception as e:
                print(f"Warning: failed to process record ID {record['id']}: {str(e)}")
                continue

        # Sort by distance (ascending)
        similarities.sort(key=lambda x: x["distance"])

        # Filter out near-identical matches (likely the query image itself)
        filtered_results = [r for r in similarities if r["distance"] > 0.5]

        # Return top-k
        results = filtered_results[:result_size]

        # Remove internal-only fields
        for result in results:
            del result["distance"]

        cursor.close()
        conn.close()

        return results

    # query_by_id() was removed in this vendored version to keep the surface area minimal.
    #     cursor = conn.cursor()
    #
    #     where_clauses = ["vector_index IS NOT NULL", "id != ?"]
    #     params = [record_id]
    #
    #     if category is not None:
    #         where_clauses.append("category = ?")
    #         params.append(category)
    #
    #     if sub_type is not None:
    #         where_clauses.append("sub_type = ?")
    #         params.append(sub_type)
    #
    #     if dataset_category is not None:
    #         where_clauses.append("dataset_category = ?")
    #         params.append(dataset_category)
    #
    #     where_clause = " AND ".join(where_clauses)
    #
    #     # Fetch matching records
    #     query_sql = f"""
    #         SELECT id, image_name, category, sub_type, with_text,
    #                image_path, generated_model, original_caption,
    #                mask_path, dataset_category, vector_index
    #         FROM papers
    #         WHERE {where_clause}
    #     """
    #
    #     cursor.execute(query_sql, params)
    #     records = cursor.fetchall()
    #
    #     # Compute similarity
    #     similarities = []
    #
    #     for record in records:
    #         try:
    #             vector_json = record["vector_index"]
    #             db_vector = json.loads(vector_json)
    #
    #             if isinstance(db_vector[0], list):
    #                 db_vector = db_vector[0]
    #
    #             distance = _cosine_distance(query_vector, db_vector)
    #
    #             result_record = {
    #                 "id": record["id"],
    #                 "image_name": record["image_name"],
    #                 "category": record["category"],
    #                 "sub_type": record["sub_type"],
    #                 "with_text": record["with_text"],
    #                 "image_path": record["image_path"],
    #                 "generated_model": record["generated_model"],
    #                 "original_caption": record["original_caption"],
    #                 "mask_path": record["mask_path"],
    #                 "dataset_category": record["dataset_category"],
    #                 "similarity_score": 1.0 - distance,
    #                 "distance": distance,
    #             }
    #
    #             similarities.append(result_record)
    #
    #         except Exception as e:
    #             print(f"Warning: failed to process record ID {record['id']}: {str(e)}")
    #             continue
    #
    #     # Sort and return results
    #     similarities.sort(key=lambda x: x["distance"])
    #     results = similarities[:result_size]
    #
    #     for result in results:
    #         del result["distance"]
    #
    #     cursor.close()
    #     conn.close()
    #
    #     return results


# if __name__ == "__main__":
#     image_b64 = ""
#
#     query_engine = VecQuery("dataset.db","facebook/dinov3-vits16-pretrain-lvd1689m")
#
#     result = query_engine.query(image_b64)
#     from pprint import pprint
#     pprint(result)
