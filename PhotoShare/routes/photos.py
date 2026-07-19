import uuid
import cloudinary

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.db import get_db
from PhotoShare.database.models import User, Role
from PhotoShare.schemas.photo import PhotoResponse, PhotoUpdate
from PhotoShare.repository.photos import (
    create_photo,
    get_photo_by_id,
    update_photo_description,
    delete_photo,
)
from PhotoShare.services.auth import auth_service
from PhotoShare.services.roles import RoleCheker
from PhotoShare.services.cloudinary_service import upload_photo
from PhotoShare.schemas.transform import TransformationParams, TransformedImageResponde
from PhotoShare.repository.transformations import create_transformd_image
from PhotoShare.repository.photos import get_photo_by_id
from PhotoShare.services.cloudinary_service import build_transformed_url, generate_qr_code


router = APIRouter(prefix="/photos", tags=["photos"])

allow_admin = RoleCheker([Role.ADMIN])


@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_new_photo(
    file: UploadFile = File(...),
    description: str | None = Form(None),
    tags: str = Form(""),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    tag_names = [t.strip() for t in tags.split(",") if t.strip()]
    if len(tag_names) > 5:
        raise HTTPException(status_code=422, detail="A photo can have a maximum of 5 tags")

    public_id = f"photoshare/{uuid.uuid4()}"
    url = upload_photo(file.file, public_id)

    photo = await create_photo(db, url, description, current_user.id, tag_names)
    return photo


@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    photo = await get_photo_by_id(db, photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo


@router.put("/{photo_id}", response_model=PhotoResponse)
async def edit_photo_description(
    photo_id: int,
    body: PhotoUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    photo = await get_photo_by_id(db, photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    if photo.owner_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    updated_photo = await update_photo_description(db, photo, body.description)
    return updated_photo


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_photo(
    photo_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    photo = await get_photo_by_id(db, photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    if photo.owner_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    await delete_photo(db, photo)

@router.post("/{photo_id}/transform", response_model=TransformedImageResponde, status_code=status.HTTP_201_CREATED)
async def transform_photo(
    photo_id: int,
    params: TransformationParams,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),

):
    photo = await get_photo_by_id(db, photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    
    if photo.owner_id != current_user.id and current_user.role !=Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission")
    
    public_id ="/".join(photo.url.split("/")[-2:]).rsplit(".", 1)[0]

    transformation_dict = params.model_dump(exclude_none=True)
    transformed_url = build_transformed_url(public_id, transformation=[transformation_dict])

    qr_public_id = f"photosahre/qr/{uuid.uuid4()}"
    qr_url = generate_qr_code(transformed_url, qr_public_id)

    transformed = await create_transformd_image(db, photo.id, transformed_url, qr_url)
    return transformed