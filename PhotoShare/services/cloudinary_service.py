import io 
import qrcode
import cloudinary
import cloudinary.uploader

from PhotoShare.conf.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure = True,
)


def upload_photo(file, public_id: str) -> str:
    result = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
    return result ["secure_url"]

def build_transformed_url(public_id: str, **transformation_params) -> str:
    url, _ = cloudinary.utils.cloudinary_url(public_id, **transformation_params)
    return url


def generate_qr_code(url: str, public_id: str) -> str:
    qr= qrcode.make(url)


    buffer = io.BytesIO()
    qr.save(buffer, "PNG")
    buffer.seek(0)

    result = cloudinary.uploader.upload(buffer, public_id=public_id, overwrite=True)
    return result["secure_url"]