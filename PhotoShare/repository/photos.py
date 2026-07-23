from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from PhotoShare.database.models import Photo, Tag



async def get_or_create_tag(db: AsyncSession, tag_name: str) -> Tag:
    result = await db.execute(select(Tag).where(Tag.name == tag_name))
    tag = result.scalar_one_or_none()

    if tag is None:
        tag = Tag(name=tag_name)
        db.add(tag)
        await db.flush()

    return tag

async def create_photo(
        db: AsyncSession,
        url: str,
        description: str | None,
        owner_id: int,
        tag_names: list[str]
) -> Photo:
    photo = Photo(url=url, description=description, owner_id=owner_id)

    for tag_name in tag_names:
        tag = await get_or_create_tag(db, tag_name)
        photo.tags.append(tag)

    db.add(photo)
    await db.commit()
    await db.refresh(photo, ["tags"])
    return photo

async def get_photo_by_id(db: AsyncSession, photo_id: int) -> Photo | None:
    result = await db.execute(
        select(Photo)
        .options(selectinload(Photo.tags))
        .where(Photo.id == photo_id)
    )
    return result.scalar_one_or_none()


async def update_photo_description(
        db: AsyncSession,
        photo: Photo,
        description: str | None
) -> Photo:
    photo.description = description
    await db.commit()
    await db.refresh(photo)
    return photo

async def delete_photo(db: AsyncSession, photo: Photo) -> None:
    await db.delete(photo)
    await db.commit()

