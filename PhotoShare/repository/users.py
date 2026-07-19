from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.models import User, Role


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str) -> User:
    result = await db.execute(select(func.count()).select_from(User))
    users_count = result.scalar()

    role = Role.ADMIN if users_count == 0 else Role.USER

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user