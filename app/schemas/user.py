from typing import List, Optional
from pydantic import BaseModel, EmailStr

from app.schemas.comment import CommentOut
from app.schemas.post import PostOut


class UserBase(BaseModel):
    username: str
    email: EmailStr
    auto_reply: bool = False
    reply_delay: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    auto_reply: Optional[bool] = None
    reply_delay: Optional[int] = None


class UserOut(UserBase):
    id: int
    is_active: bool = True
    posts: List[PostOut] = []
    comments: List[CommentOut] = []

    class Config:
        orm_mode = True
