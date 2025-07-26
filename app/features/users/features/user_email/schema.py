from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UserEmailResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    email: str
    create_date: datetime
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)