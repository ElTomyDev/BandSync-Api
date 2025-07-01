from pydantic import BaseModel, Field

class RegisterUserSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=3, max_length=20)
    description: str | None = Field(..., max_length=250)

class UserResponseSchema(BaseModel):
    name: str
    lastname: str
    username: str