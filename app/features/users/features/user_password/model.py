from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class UserPasswordModel(BaseModel):
    id: ObjectId = Field(default_factory=lambda: ObjectId(), alias="_id")
    user_id: ObjectId
    password: str
    password_reset_token: str | None = None
    password_reset_expiry: str | None = None
    last_update: datetime | None = None
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)