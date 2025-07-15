from app.enums.account_state_enum import AccountStates
from app.enums.role_enum import MusicalRoles
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from bson.objectid import ObjectId

class UserModel(BaseModel):
    id: ObjectId = Field(default_factory=lambda: ObjectId(), alias="_id")
    location_id: ObjectId = Field(default=None)
    social_id: ObjectId = Field(default=None)
    image_url: str | None = Field(default=None)
    musical_role: MusicalRoles = Field(default=MusicalRoles.NONE)
    name: str
    lastname: str
    username: str
    description: str | None = Field(default=None)
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_connection: datetime | None = Field(default=None)
    account_state: AccountStates = Field(default=AccountStates.ACTIVE)
    phone_number: str | None = Field(default=None)
    last_failed_login: datetime | None = Field(default=None)
    failed_login_attempts: int = Field(default=0)
    find_bands: bool = Field(default=False)
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)