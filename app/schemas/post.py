from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.comment import CommentOut


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    created_at: datetime
    is_blocked: bool
    owner_id: int
    comments: List[CommentOut] = []

    class Config:
        orm_mode = True
