from dataclasses import Field

from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)