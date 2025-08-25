from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field


class EmailAuthModel(BaseModel):
    email: str
    email_verified: bool = Field(default=False)
    email_verification_token_hash: str | None = Field(default=None)
    email_verification_expiry: datetime | None = Field(default=None)
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        serialize_by_alias=True)