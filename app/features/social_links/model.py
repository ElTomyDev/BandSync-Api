from pydantic import BaseModel, ConfigDict

class SocialLinksModel(BaseModel):
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
        serialize_by_alias=True)
    