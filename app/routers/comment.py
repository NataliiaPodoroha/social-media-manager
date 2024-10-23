from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.schemas.comment import CommentCreate, CommentOut, CommentAnalytics
from dependencies import get_db
from app.auth.auth import get_current_active_user
from app.crud.comment import (
    create_comment,
    get_comment,
    get_comments_by_user,
    get_comments_by_post,
    delete_comment,
    get_comment_analytics,
)
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=CommentOut)
def create_new_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_comment(db=db, comment=comment, user_id=current_user.id)


@router.get("/{comment_id}/", response_model=CommentOut)
def read_single_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment(db=db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.get("/users/{user_id}/comments/", response_model=List[CommentOut])
def read_comments_by_user(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return get_comments_by_user(db=db, user_id=user_id, skip=skip, limit=limit)


@router.get("/posts/{post_id}/comments/", response_model=List[CommentOut])
def read_comments_by_post(
    post_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return get_comments_by_post(db=db, post_id=post_id, skip=skip, limit=limit)


@router.delete("/{comment_id}/", status_code=204)
def delete_comment_endpoint(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_comment = get_comment(db=db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )

    delete_comment(db=db, comment_id=comment_id)


@router.get("/analytics/daily-stats", response_model=List[CommentAnalytics])
def get_comments_analytics(
        date_from: datetime = Query(
            ..., description="Start date for the period (YYYY-MM-DD)"
        ),
        date_to: datetime = Query(..., description="End date for the period (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    return get_comment_analytics(db=db, date_from=date_from, date_to=date_to)
