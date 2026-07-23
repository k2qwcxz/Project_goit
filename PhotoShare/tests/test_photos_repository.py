import pytest
from PhotoShare.repository.photos import create_photo, get_photo_by_id, delete_photo
from PhotoShare.repository.users import create_user


@pytest.mark.asyncio
async def test_create_photo_with_tags(db_session):
    user = await create_user(db_session, "photouser", "photo@test.com", "hashed_pw")

    photo = await create_photo(
        db_session,
        url="https://cloudinary.com/test.jpg",
        description="Photo with tags",
        owner_id=user.id,
        tag_names=["sunset", "beach"],
    )



    tag_names = [tag.name for tag in photo.tags]
    assert "sunset" in tag_names
    assert "beach" in tag_names
    assert len(photo.tags) == 2




@pytest.mark.asyncio
async def test_reused_tag_is_not_duplicated(db_session):

    user = await create_user(db_session, "photouser2", "photo2@test.com", "hashed_pw")

    photo1 = await create_photo(
        db_session, "https://cloudinary.com/a.jpg", None, user.id, ["nature"]
    )
    photo2 = await create_photo(
        db_session, "https://cloudinary.com/b.jpg", None, user.id, ["nature"]
    )


    assert photo1.tags[0].id == photo2.tags[0].id

@pytest.mark.asyncio
async def test_delete_photo(db_session):
    user = await create_user(db_session, "photouser3", "photo3@test.com", "hashed_pw")
    photo = await create_photo(db_session, "https://cloudinary.com/d.jpg", None, user.id, [])
    photo_id = photo.id

    await delete_photo(db_session, photo)

    result = await get_photo_by_id(db_session, photo_id)
    assert result is None
