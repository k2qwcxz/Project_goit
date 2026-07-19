from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    avatar: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str 


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserRegisterResponse(BaseModel):
    user: UserResponse
    details: str = "User registered successfully"


