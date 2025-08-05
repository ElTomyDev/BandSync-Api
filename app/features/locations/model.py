from pydantic import BaseModel, ConfigDict, Field


class LocationModel(BaseModel):
    country: str | None = Field(default=None)
    state: str | None = Field(default=None)
    city: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    address: str | None = Field(default=None)
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)