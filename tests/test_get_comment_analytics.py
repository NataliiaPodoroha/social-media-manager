from datetime import datetime, timedelta

from app.crud.comment import get_comment_analytics
from app.models.comment import Comment


def test_no_comments(db):
    date_from = datetime(2024, 1, 1, 1, 1, 1)
    date_to = datetime(2024, 1, 3, 1, 1, 1)

    comment_not_in_range = Comment(
        content="Test comment",
        created_at=datetime(2023, 1, 1, 1, 1, 1),
        is_blocked=False,
    )

    db.add_all([comment_not_in_range])
    db.commit()

    result = get_comment_analytics(db, date_from, date_to)
    assert result == []


def test_comments_multiple_days(db):
    date_from = datetime(2024, 1, 1, 1, 1, 1)
    date_to = datetime(2024, 1, 7, 1, 1, 1)

    comment_not_in_range = Comment(
        content="Test comment",
        created_at=datetime(2023, 1, 1, 1, 1, 1),
        is_blocked=False,
    )

    comment_day_1 = Comment(
        content="Test comment 2",
        created_at=datetime(2024, 1, 1, 1, 1, 2),
        is_blocked=False,
    )

    comment_blocked_day_1 = Comment(
        content="Test comment 1",
        created_at=datetime(2024, 1, 1, 1, 1, 1),
        is_blocked=True,
    )

    comment_day_2 = Comment(
        content="Test comment 2",
        created_at=datetime(2024, 1, 2, 1, 1, 2),
        is_blocked=False,
    )

    comment_blocked_day_3 = Comment(
        content="Test comment 1",
        created_at=datetime(2024, 1, 3, 1, 1, 1),
        is_blocked=True,
    )

    db.add_all(
        [
            comment_not_in_range,
            comment_day_1,
            comment_blocked_day_1,
            comment_day_2,
            comment_blocked_day_3,
        ]
    )
    db.commit()
    result = get_comment_analytics(db, date_from, date_to)
    assert len(result) == 3

    assert result[0].date == "2024-01-01"
    assert result[0].created_comments == 2
    assert result[0].blocked_comments == 1

    assert result[1].date == "2024-01-02"
    assert result[1].created_comments == 1
    assert result[1].blocked_comments == 0

    assert result[2].date == "2024-01-03"
    assert result[2].created_comments == 1
    assert result[2].blocked_comments == 1

