from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from app.utils.object_id import ObjectIdPydanticAnnotation

class UpdateSocialLinksSchema(BaseModel):
    instagram: Optional[str] = Field(default=None, max_length=255)
    facebook: Optional[str] = Field(default=None, max_length=255)
    x: Optional[str] = Field(default=None, max_length=255)
    tiktok: Optional[str] = Field(default=None, max_length=255)
    reddit: Optional[str] = Field(default=None, max_length=255)
    youtube: Optional[str] = Field(default=None, max_length=255)
    spotify: Optional[str] = Field(default=None, max_length=255)
    soundcloud: Optional[str] = Field(default=None, max_length=255)
    bandcamp: Optional[str] = Field(default=None, max_length=255)
    
class SocialLinksResponseSchema(BaseModel):
    instagram: str | None
    facebook: str | None
    x: str | None
    tiktok: str | None
    reddit: str | None
    youtube: str | None
    spotify: str | None
    soundcloud: str | None
    bandcamp: str | None