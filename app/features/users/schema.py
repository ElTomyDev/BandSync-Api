from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UserFindSchema(BaseModel):
    id: Optional[str] = Field(None)
    username: Optional[str] = Field(None)

class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6, max_length=255)
    email: str = Field(..., max_length=150)
    description: str | None = Field(None, max_length=250)

class UpdateDescriptionSchema(BaseModel):
    new_description: str = Field(..., max_length=250)
    
class UpdatePhoneNumberSchema(BaseModel):
    new_phone_number: str = Field(..., max_length=25)

class UpdateNameSchema(BaseModel):
    new_name: str = Field(..., max_length=50)

class UpdateLastnameSchema(BaseModel):
    new_lastname: str = Field(..., max_length=50)

class UpdateUsernameSchema(BaseModel):
    new_username: str = Field(..., max_length=20)

class UserResponseSchema(BaseModel):
    id: str = Field(alias='_id')
    name: str
    lastname: str
    username: str
    
    model_config = ConfigDict(serialize_by_alias=True)