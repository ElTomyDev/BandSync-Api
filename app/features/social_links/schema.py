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
    