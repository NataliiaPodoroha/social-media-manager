from datetime import datetime
from typing import List
from sqlalchemy import func, case
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException

from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentAnalytics
from app.services.moderation import moderate_text
from app.services.ai_responder import generate_ai_reply


def moderate_comment(content: str) -> bool:
    return moderate_text(content)


def create_db_comment(db: Session, comment: CommentCreate, user_id: int, is_blocked: bool) -> Comment:
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        owner_id=user_id,
        is_blocked=is_blocked,
        parent_comment_id=comment.parent_comment_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def handle_ai_reply(db: Session, comment: CommentCreate, user_id: int, parent_comment_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.auto_reply:
        post = db.query(Post).filter(Post.id == comment.post_id).first()
        post_content = post.content if post else ""
        ai_reply = generate_ai_reply(post_content, comment.content, user_id, db)

        db_reply = Comment(
            content=ai_reply,
            post_id=comment.post_id,
            owner_id=user_id,
            is_blocked=False,
            parent_comment_id=parent_comment_id,
        )
        db.add(db_reply)
        db.commit()


def create_comment(db: Session, comment: CommentCreate, user_id: int) -> Comment:
    is_approved = moderate_comment(comment.content)

    if not is_approved:
        raise HTTPException(
            status_code=400,
            detail="Comment contains inappropriate content and is blocked.",
        )

    db_comment = create_db_comment(db, comment, user_id, is_blocked=not is_approved)
    handle_ai_reply(db, comment, user_id, db_comment.id)
    return db_comment


def get_comment(db: Session, comment_id: int) -> Comment:
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment or db_comment.is_blocked:
        raise HTTPException(status_code=404, detail="Comment not found or blocked.")
    return db_comment


def get_comments_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
    return (
        db.query(Comment)
        .filter(Comment.owner_id == user_id, Comment.is_blocked == False)
        .options(selectinload(Comment.post))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id, Comment.is_blocked == False)
        .options(selectinload(Comment.owner))
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_comment(db: Session, comment_id: int) -> None:
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found.")
    db.delete(db_comment)
    db.commit()


def get_comment_analytics(db: Session, date_from: datetime, date_to: datetime) -> List[CommentAnalytics]:
    return (
        db.query(
            func.date(Comment.created_at).label("date"),
            func.count(Comment.id).label("created_comments"),
            func.sum(case((Comment.is_blocked == True, 1), else_=0)).label("blocked_comments")
        )
        .filter(Comment.created_at.between(date_from, date_to))
        .group_by(func.date(Comment.created_at))
        .order_by(func.date(Comment.created_at))
        .all()
    )
