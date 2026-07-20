from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.models import Comment


async def create_comment(db: AsyncSession, photo_id: int, user_id: int, text: str)-> Comment:
    comment = Comment(photo_id=photo_id, user_id=user_id, text=text)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Comment | None:
    result = await db.execute(select(Comment). where(Comment.id == comment_id))
    return result.scalar_one_or_none()

async def update_comment(db: AsyncSession, comment: Comment, text: str) -> Comment:
    comment.text = text
    await db.commit()
    await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment: Comment) -> None:
    await db.delete(comment)
    await db.commit()