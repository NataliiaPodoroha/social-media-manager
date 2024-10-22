from unittest.mock import patch

from sqlalchemy.orm import Session
from app.crud.comment import create_comment
from app.models.user import User
from app.schemas.comment import CommentCreate
from app.models.comment import Comment


def test_create_comment_success(db: Session):
    comment_data = CommentCreate(
        content="Valid content", post_id=1, parent_comment_id=None
    )
    comment = create_comment(db, comment_data, 77)

    assert comment.id is not None
    assert comment.content == comment_data.content
    assert comment.post_id == comment_data.post_id
    assert comment.owner_id == 77
    assert comment.is_blocked is False


def test_create_comment_blocked(db: Session):
    comment_data = CommentCreate(content="sh1t", post_id=1, parent_comment_id=None)
    comment = create_comment(db, comment_data, 77)

    assert comment.id is not None
    assert comment.content == comment_data.content
    assert comment.post_id == comment_data.post_id
    assert comment.owner_id == 77
    assert comment.is_blocked is True


@patch("app.crud.comment.generate_ai_reply")
def test_create_comment_with_ai_reply(mock_generate_ai_reply, db: Session):
    user = User(
        username="John Doe",
        email="jdoe@test.com",
        hashed_password="#abc123",
        auto_reply=True,
        reply_delay=0.2,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    mock_generate_ai_reply.return_value = "This is an AI generated reply."

    comment_data = CommentCreate(
        content="Valid content", post_id=1, parent_comment_id=None
    )
    comment = create_comment(db, comment_data, user.id)

    assert comment.id is not None
    assert comment.content == comment_data.content
    assert comment.post_id == comment_data.post_id
    assert comment.owner_id == user.id
    assert comment.is_blocked is False

    ai_reply = db.query(Comment).filter(Comment.parent_comment_id == comment.id).first()
    assert ai_reply is not None
    assert ai_reply.content == "This is an AI generated reply."
    assert ai_reply.parent_comment_id == comment.id
    assert ai_reply.post_id == comment_data.post_id
    assert ai_reply.owner_id == user.id
    assert ai_reply.is_blocked is False
