import pytest
from PhotoShare.repository.comments import (
    create_comment,
    update_comment,
    delete_comment,
)
from PhotoShare.repository.photos import create_photo
from PhotoShare.repository.users import create_user

@pytest.mark.asyncio
async def test_create_comment(db_session):
    user = await create_user(db_session, "commentuser", "comment@test.com", "hashed_pw")
    photo = await create_photo(db_session, "https://cloudinary.com/x.jpg", None, user.id, [])

    comment = await create_comment(db_session, photo.id, user.id, "Nice photo!")

    assert comment.id is not None
    assert comment.text == "Nice photo!"
    assert comment.photo_id == photo.id
    assert comment.user_id == user.id
    assert comment.created_at is not None



@pytest.mark.asyncio
async def test_update_comment_changes_updated_at(db_session):
    user = await create_user(db_session, "commentuser3", "comment3@test.com", "hashed_pw")
    photo = await create_photo(db_session, "https://cloudinary.com/z.jpg", None, user.id, [])
    comment = await create_comment(db_session, photo.id, user.id, "Text")

    original_updated_at = comment.updated_at

    updated = await update_comment(db_session, comment, "New text")

    assert updated.updated_at >= original_updated_at

