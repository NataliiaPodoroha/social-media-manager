from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.comment import Comment
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    auto_reply = Column(Boolean, default=False)
    reply_delay = Column(Integer, default=60)
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
