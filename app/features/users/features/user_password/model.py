from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class UserPasswordModel(BaseModel):
    id: ObjectId = Field(default_factory=lambda: ObjectId(), alias="_id")
    id_user: ObjectId = Field(default=None)
    password: str
    password_reset_token: str | None = Field(dafault=None)
    password_reset_expiry: str | None = Field(default=None)
    last_update: datetime | None = Field(default=None)
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)