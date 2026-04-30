from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel


class Forgeryscope(BaseModel):
    answer: Literal["A", "B", "C", "D"]


class Visualtext(BaseModel):
    answer: Literal["A", "B"]


class Manipulation(BaseModel):
    answer: Literal["A", "B", "C", "D"]


class Any(BaseModel):
    pass

