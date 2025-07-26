
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class UserEmailModel(BaseModel):
    id: ObjectId = Field(default_factory=lambda: ObjectId(), alias="_id")
    user_id: ObjectId
    email: str
    email_verified: bool = Field(default=False)
    email_verification_token: str | None = Field(default=None)
    email_verification_expiry: datetime | None = Field(default=None)
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)