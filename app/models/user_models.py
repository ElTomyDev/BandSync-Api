from pydantic import BaseModel, Field
from bson import ObjectId
from app.enums.role_enum import MusicalRoles
from app.enums.account_state_enum import AccountStates
from datetime import datetime, timezone

class UserModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId), alias="_id")
    id_location: str | None = None
    id_social: str | None = None
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
    
     
    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True