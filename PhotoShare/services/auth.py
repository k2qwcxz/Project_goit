from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from PhotoShare.database.db import get_db
from PhotoShare.conf.config import settings
from PhotoShare.repository.users import get_user_by_email


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    oauth2_scheme = HTTPBearer()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire, "scope": "access_token"})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
    

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire, "scope": "refresh_token"})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)


    async def decode_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "refresh_token":
                return payload["sub"]
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def decode_refresh_token(self, refresh_token: str) -> str:
        return await self.decode_token(refresh_token)
        

    async def get_current_user(self, token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token_value = token.credentials

        try:
            payload = jwt.decode(token_value, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "access_token":
                email: str = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = await get_user_by_email(db, email)
        if user is None:
            raise credentials_exception
        
        return user
    
auth_service = Auth()

        

        




