from sqlalchemy.orm import Session
from app.crud.post import create_post
from app.schemas.post import PostCreate


def test_create_post_success(db: Session):
    post_data = PostCreate(title="Valid Title", content="Valid content")
    post = create_post(db, post_data, 77)

    assert post.id is not None
    assert post.title == post_data.title
    assert post.content == post_data.content
    assert post.owner_id == 77
    assert post.is_blocked is False


def test_create_post_blocked(db: Session):
    post_data = PostCreate(title="Blocked", content="sh1t")
    post = create_post(db, post_data, 77)

    assert post.id is not None
    assert post.title == post_data.title
    assert post.content == post_data.content
    assert post.owner_id == 77
    assert post.is_blocked is True



