from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from app.utils.object_id import ObjectIdPydanticAnnotation

class SocialLinkUpdateSchema(BaseModel):
    instagram: str | None = Field(None, max_length=255)
    facebook: str | None = Field(None, max_length=255)
    x: str | None = Field(None, max_length=255)
    tiktok: str | None = Field(None, max_length=255)
    reddit: str | None = Field(None, max_length=255)
    youtube: str | None = Field(None, max_length=255)
    spotify: str | None = Field(None, max_length=255)
    soundcloud: str | None = Field(None, max_length=255)
    bandcamp: str | None = Field(None, max_length=255)
    
class SocialLinkResposeSchema(BaseModel):
    instagram: str | None
    facebook: str | None
    x: str | None
    tiktok: str | None
    reddit: str | None
    youtube: str | None
    spotify: str | None
    soundcloud: str | None
    bandcamp: str | None