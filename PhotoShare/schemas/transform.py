from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TransformationParams(BaseModel):
    width: int | None = Field(None, gt=0, le=2000)
    height: int | None = Field(None, gt=0, le=2000)
    crop: str  | None = None 
    effect: str | None = None 
    radius: int | None = Field(None, ge=0, le=1000)


class TransformedImageResponde(BaseModel):
    id: int
    photo_id: int
    url: str
    qr_code_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)















