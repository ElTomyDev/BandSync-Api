from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from bson import ObjectId

class SocialLinkModel(BaseModel):
    id: Optional[str] = Field(default=str(ObjectId()), alias="_id")
    instagram: str | None = None
    facebook: str | None = None
    x: str | None = None
    tiktok: str | None = None
    reddit: str | None = None
    youtube: str | None = None
    spotify: str | None = None
    soundcloud: str | None = None
    bandcamp: str | None = None
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True
    )
    