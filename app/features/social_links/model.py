from pydantic import BaseModel, ConfigDict
from bson import ObjectId

class SocialLinkModel(BaseModel):
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
        arbitrary_types_allowed = True
    )
    