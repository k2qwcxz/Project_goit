from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.db import get_db
from PhotoShare.database.models import User, Role
from PhotoShare.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from PhotoShare.repository.comments import (
    create_comment,
    get_comment_by_id,
    update_comment,
    delete_comment,
)
from PhotoShare.repository.photos import get_photo_by_id
from PhotoShare.services.auth import auth_service
from PhotoShare.services.roles import RoleCheker

router = APIRouter(tags=["comments"])

allow_moderation = RoleCheker([Role.ADMIN, Role.MODERATOR])

@router.post("/photos/{photo_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    photo_id:int,
    body: CommentCreate,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db)

):
    photo = await get_photo_by_id(db, photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    
    comment = await create_comment(db, photo_id, current_user.id, body.text)
    return comment


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def edit_comment(
    comment_id: int,
    body: CommentUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    comment = await get_comment_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can edit only your own comments")
    
    update = await update_comment(db, comment, body.text)
    return update


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_comment(
    comment_id: int,
    current_user: User = Depends(allow_moderation),
    db: AsyncSession = Depends(get_db),
):
    comment = await get_comment_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    await delete_comment(db, comment)
