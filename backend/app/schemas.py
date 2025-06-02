from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostCreate(BaseModel):

    title: str
    text: str
    file: str = None
    photo: str = None
    author: str
    date: str = None


class DisciplineCreate(BaseModel):

    title: str