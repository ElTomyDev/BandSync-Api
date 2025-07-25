from bson import ObjectId
from fastapi import Request
from app.features.users.features.user_password.model import UserPasswordModel
from app.features.users.features.user_password.repository import UserPasswordRepository
from passlib.hash import bcrypt

from app.features.users.model import UserModel

class UserPasswordService:
    def __init__(self, request: Request):
        self.__repository = UserPasswordRepository(request)
    
    async def create_password_document(self, user_model: UserModel, password: str) -> None:
        user_password = UserPasswordModel(id_user=user_model.id, password=bcrypt.hash(password))
        await self.__repository.insert_one(user_password)
    
    