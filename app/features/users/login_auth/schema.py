from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    email: str|None = Field(None)
    username: str|None = Field(None)
    password: str

class LoginTokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"