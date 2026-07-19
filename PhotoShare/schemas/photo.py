from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

class PhotoCreate(BaseModel):
    description: str | None = None
    tags: list[str] 


    @field_validator("tags")
    @classmethod
    def validate_tags_count(cls, value: list[str]) -> list[str]:
        if len(value) > 5:
            raise ValueError("A maximum of 5 tags is allowed.")
        return value
    
class PhotoUpdate(BaseModel):
    description: str | None = None

class TagResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class PhotoResponse(BaseModel):
    id: int
    url: str
    description: str | None = None
    owner_id: int
    tags: list[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)




















