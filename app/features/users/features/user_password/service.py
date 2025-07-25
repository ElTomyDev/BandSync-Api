from bson import ObjectId
from fastapi import HTTPException, Request
from app.features.users.features.user_password.model import UserPasswordModel
from app.features.users.features.user_password.repository import UserPasswordRepository
from passlib.hash import bcrypt

from app.features.users.features.user_password.schema import UserPasswordUpdateSchema
from app.features.users.model import UserModel

class UserPasswordService:
    def __init__(self, request: Request):
        self.__repository = UserPasswordRepository(request)
    
    async def create_password_document(self, user_model: UserModel, password: str) -> None:
        user_password = UserPasswordModel(
            user_id = user_model.id, 
            password = bcrypt.hash(password)
        )
        await self.__repository.insert_one(user_password)
    
    async def __find_password_document(self, user_model: UserModel) -> UserPasswordModel:
        password = await self.__repository.find_by_user_id(user_model.id)
        if password == None:
            raise HTTPException(status_code=404, detail=f"The password with user_id '{str(user_model.id)}' not found")
        return password
    
    async def update_password_document(self, user_model: UserModel, password_update_schema: UserPasswordUpdateSchema) -> None:
        password_document = await self.__find_password_document(user_model)
        
        if not bcrypt.verify(password_update_schema.old_password, password_document.password):
            raise HTTPException(status_code=403, detail="The password is incorrect")
        
        await self.__repository.update_password_by_user_id(user_model.id, bcrypt.hash(password_update_schema.new_password))
    
    