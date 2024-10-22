from datetime import datetime

from typing import List

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    post_id: int
    parent_comment_id: int | None = None


class CommentCreate(CommentBase):
    pass


class CommentAnalytics(BaseModel):
    date: datetime
    created_comments: int
    blocked_comments: int


class CommentOut(CommentBase):
    id: int
    owner_id: int
    is_blocked: bool
    created_at: datetime
    replies: List["CommentOut"] = []

    class Config:
        orm_mode = True
