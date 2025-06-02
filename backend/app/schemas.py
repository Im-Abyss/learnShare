from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostCreate(BaseModel):

    text: str
    file: str = None
    photo: str = None
    author: str
    date: str = None


class PostResponse(PostCreate):
    id: int
    discipline_id: int
    date: str