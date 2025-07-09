from typing import Optional
from pydantic import BaseModel, Field

class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=3, max_length=20)
    description: str | None = Field(..., max_length=250)

class UserResponseSchema(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    lastname: str
    username: str