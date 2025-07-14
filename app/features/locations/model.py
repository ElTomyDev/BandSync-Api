from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Location(BaseModel):
    id: ObjectId = Field(default_factory= lambda: ObjectId(), alias="_id")
    country: str | None = Field(default=None)
    state: str | None = Field(default=None)
    city: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    address: str | None = Field(default=None)
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)