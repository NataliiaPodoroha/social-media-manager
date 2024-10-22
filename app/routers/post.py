from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.post import PostCreate, PostOut
from app.crud.post import (
    create_post,
    get_all_posts,
    get_single_post,
    get_posts_by_owner,
    delete_post
)
from app.auth.auth import get_current_active_user
from app.models.user import User
from dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[PostOut])
def read_all_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_all_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}/", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = get_single_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/user/{user_id}/", response_model=List[PostOut])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts_by_owner(db, user_id=user_id, skip=skip, limit=limit)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")
    return posts


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_new_post(
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):
    db_post = create_post(db=db, post=post, user_id=current_user.id)
    return db_post


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):
    post = get_single_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    delete_post(db, post_id)
    return {"detail": "Post deleted"}
