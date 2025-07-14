from app.enums.account_state_enum import AccountStates
from app.enums.role_enum import MusicalRoles
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from bson.objectid import ObjectId

class UserModel(BaseModel):
    id: ObjectId = Field(default_factory=lambda: ObjectId(), alias="_id")
    location_id: ObjectId = Field(default=None)
    social_id: ObjectId = Field(default=None)
    image_url: str | None = None
    musical_role: MusicalRoles = MusicalRoles.NONE
    name: str
    lastname: str
    username: str
    description: str | None = None
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_connection: datetime | None = None
    account_state: AccountStates = AccountStates.ACTIVE
    phone_number: str | None = None
    last_failed_login: datetime | None = None
    failed_login_attempts: int = 0
    find_bands: bool = False
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)