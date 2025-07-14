from pydantic import BaseModel, Field

class LocationUpdateSchema(BaseModel):
    country: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=150)
    
class LocationResponseSchema(BaseModel):
    country: str | None
    state: str | None
    city: str | None
    postal_code: str | None
    address: str | None
    