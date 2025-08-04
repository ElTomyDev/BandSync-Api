from bson import ObjectId
from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field
from app.utils.object_id import ObjectIdPydanticAnnotation

class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6, max_length=255)
    email: str = Field(..., max_length=150)
    description: str | None = Field(None, max_length=250)

class UpdatePasswordSchema(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(..., min_length=6, max_length=255)

class UserResponseSchema(BaseModel):
    id: str = Field(alias='_id')
    name: str
    lastname: str
    username: str
    
    model_config = ConfigDict(serialize_by_alias=True)