from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate
from app.services.moderation import moderate_text


def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
    is_blocked = not (
        moderate_text(post.content) and moderate_text(post.title)
    )

    db_post = Post(**post.dict(), owner_id=user_id, is_blocked=is_blocked)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_all_posts(db: Session, skip: int = 0, limit: int = 10) -> list[Post]:
    return (
        db.query(Post).filter(
            Post.is_blocked == False
        ).offset(skip).limit(limit).all()
    )


def get_single_post(db: Session, post_id: int) -> Post:
    post = db.query(Post).filter(
        Post.id == post_id, Post.is_blocked == False
    ).first()
    if not post:
        raise HTTPException(
            status_code=403,
            detail="This post has been blocked or does not exist.",
        )
    return post


def get_posts_by_owner(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> list[Post]:
    return (
        db.query(Post)
        .filter(Post.owner_id == user_id, Post.is_blocked == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_post(db: Session, post_id: int) -> None:
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
