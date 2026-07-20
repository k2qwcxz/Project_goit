from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    text:str

class CommentUpdate(BaseModel):
    text:str

class CommentResponse(BaseModel):
    id:int
    text:str
    photo_id:int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



