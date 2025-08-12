from app.enums.account_state_enum import AccountStates
from app.enums.role_enum import MusicalRoles
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from bson.objectid import ObjectId

from app.features.locations.model import LocationModel
from app.features.social_links.model import SocialLinksModel
from app.features.users.email_auth.model import EmailAuthModel
from app.features.users.login_auth.model import LoginAuthModel
from app.features.users.password_auth.model import PasswordAuthModel

class UserModel(BaseModel):
    id: ObjectId = Field(default_factory=lambda: ObjectId(), alias="_id")
    image_url: str | None = Field(default=None)
    name: str
    lastname: str
    username: str
    phone_number: str | None = Field(default=None)
    description: str | None = Field(default=None)
    find_bands: bool = Field(default=False)
    musical_role: MusicalRoles = Field(default=MusicalRoles.NONE)
    account_state: AccountStates = Field(default=AccountStates.ACTIVE)
    location: LocationModel
    social_links: SocialLinksModel
    login_auth: LoginAuthModel
    email_auth: EmailAuthModel
    password_auth: PasswordAuthModel
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)