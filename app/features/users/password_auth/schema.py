from pydantic import BaseModel, Field


class UpdatePasswordSchema(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(..., min_length=6, max_length=255)