from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from PhotoShare.conf.config import settings

engine = create_async_engine(settings.DB_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

