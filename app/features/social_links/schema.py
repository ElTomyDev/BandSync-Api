from typing import Optional
from pydantic import BaseModel, Field


class SocialLinkUpdateSchema(BaseModel):
    instagram: str | None = Field(..., max_length=255)
    facebook: str | None = Field(..., max_length=255)
    x: str | None = Field(..., max_length=255)
    tiktok: str | None = Field(..., max_length=255)
    reddit: str | None = Field(..., max_length=255)
    youtube: str | None = Field(..., max_length=255)
    spotify: str | None = Field(..., max_length=255)
    soundcloud: str | None = Field(..., max_length=255)
    bandcamp: str | None = Field(..., max_length=255)
    
class SocialLinkResposeSchema(BaseModel):
    id: Optional[str] = Field(alias="_id")
    instagram: str | None
    facebook: str | None
    x: str | None
    tiktok: str | None
    reddit: str | None
    youtube: str | None
    spotify: str | None
    soundcloud: str | None
    bandcamp: str | None
    