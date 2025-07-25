from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UserPasswordUpdateSchema(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(..., min_length=6, max_length=255)

class UserPasswordResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    id_user: str
    create_date: datetime
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)
    