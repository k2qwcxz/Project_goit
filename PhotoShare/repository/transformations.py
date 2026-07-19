from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.models import TransformedImage

async def create_transformd_image(
        db: AsyncSession, 
        photo_id: int,
        url: str,
        qr_code_url: str,
) -> TransformedImage:
    transdormed = TransformedImage(
        photo_id = photo_id,
        url = url,
        qr_code_url = qr_code_url
    )
    db.add(transdormed)
    await db.commit()
    await db.refresh(transdormed)

    return transdormed
    