from typing import Any

from fastapi import HTTPException, Request
from passlib.hash import bcrypt

from app.features.users.model import UserModel
from app.features.users.password_auth.model import PasswordAuthModel
from app.features.users.password_auth.repository import PasswordAuthRepository
from app.features.users.schema import UpdatePasswordSchema

class PasswordAuthService:
    def __init__(self, request: Request):
        self.__repository = PasswordAuthRepository(request)
        
    async def create_password_model(self, password: str) -> dict[str, Any]:
        user_password = PasswordAuthModel(
            password = bcrypt.hash(password)
        )
        return user_password
    
    async def update_password(self, user_model: UserModel, old_password: str, new_password: str) -> None:
        if not bcrypt.verify(old_password, user_model.password_auth['password']):
            raise HTTPException(status_code=400, detail="The password is incorrect")
        
        update_result = await self.__repository.update_password(user_model.id, bcrypt.hash(new_password))
        
        if update_result.modified_count == 0:
            raise HTTPException(status_code=500, detail="The password could not be updated")