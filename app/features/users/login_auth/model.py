from datetime import datetime

from pydantic import BaseModel, Field


class LoginAuthModel(BaseModel):
    last_failed_login: datetime | None = Field(default=None)
    failed_login_attempts: int = Field(default=0)
    last_connection: datetime | None = Field(default=None)