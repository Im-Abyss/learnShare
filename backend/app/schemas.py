from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostCreate(BaseModel):

    title: str
    content: str
    author: str
    date: Optional[str] = None


class PostResponse(PostCreate):
    id: int
    discipline_id: int
    date: str