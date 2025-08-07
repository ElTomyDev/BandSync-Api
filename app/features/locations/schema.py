from typing import Optional
from pydantic import BaseModel, Field

class LocationUpdateSchema(BaseModel):
    country: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    postal_code: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=150)
    
class LocationResponseSchema(BaseModel):
    country: str | None
    state: str | None
    city: str | None
    postal_code: str | None
    address: str | None
    