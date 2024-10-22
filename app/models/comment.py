from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_blocked = Column(Boolean, default=False)
    parent_comment_id = Column(
        Integer, ForeignKey("comments.id"), nullable=True
    )

    post = relationship("Post", back_populates="comments")
    owner = relationship("User", back_populates="comments")
    parent_comment = relationship(
        "Comment", remote_side=[id], back_populates="replies"
    )
    replies = relationship("Comment", back_populates="parent_comment")
