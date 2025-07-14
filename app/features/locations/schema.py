from pydantic import BaseModel, Field


class LocationUpdateSchema(BaseModel):
    country: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=150)
    
class LocationResponseSchema(BaseModel):
    country: str
    state: str
    city: str
    postal_code: str
    address: str