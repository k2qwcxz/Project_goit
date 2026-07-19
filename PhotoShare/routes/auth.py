from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession


from PhotoShare.database.db import get_db
from PhotoShare.repository.users import get_user_by_email, create_user
from PhotoShare.schemas.user import UserCreate, UserRegisterResponse, UserResponse, Token
from PhotoShare.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()  # Initialize the HTTPBearer security scheme

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    hashed_password = auth_service.get_password_hash(user.password)
    new_user = await create_user(db, user.username, user.email, hashed_password)

    return UserRegisterResponse(user=UserResponse.model_validate(new_user))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    

    if not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = auth_service.create_access_token(data={"sub": user.email})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})

    return{
        "access_token": await access_token,
        "refresh_token": await refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh_token", response_model=Token)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await get_user_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    

    new_access_token = auth_service.create_access_token(data={"sub": user.email})
    new_refresh_token = auth_service.create_refresh_token(data={"sub": user.email})


    return {
        "access_token": await new_access_token,
        "refresh_token": await new_refresh_token,
        "token_type": "bearer"
    }