from pydantic import BaseModel
from typing import Literal, List


class Forgeryscope(BaseModel):
    answer: Literal["A", "B", "C", "D"]
    reason: str


class Visualtext(BaseModel):
    answer: Literal["A", "B"]
    reason: str


class Manipulation(BaseModel):
    answer: Literal["A", "B", "C", "D"]
    reason: str


class Pinpointing(BaseModel):
    bboxes: List[List[float]]
    reason: str


class Any(BaseModel):
    pass
