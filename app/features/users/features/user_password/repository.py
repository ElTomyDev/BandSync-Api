from datetime import datetime, timezone
from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult

from app.features.users.features.user_password.model import UserPasswordModel


class UserPasswordRepository:
    def __init__(self, request: Request):
        self.__passwords_collection = request.app.state.db['user_passwords']
    
    async def insert_one(self, password_model: UserPasswordModel) -> None:
        await self.__passwords_collection.insert_one(password_model.model_dump())
    
    async def find_by_user_id(self, user_id: ObjectId) -> UserPasswordModel | None:
        password = await self.__passwords_collection.find_one({'user_id': ObjectId(user_id)})
        
        if password:
            return UserPasswordModel(**password)
        return None
    
    async def update_password_by_user_id(self, user_id: ObjectId, new_password: str) -> UpdateResult:
        result = await self.__passwords_collection.update_one(
            {"user_id": user_id},
            {"$set":{
                'password': new_password,
                "last_update": datetime.now(timezone.utc)
                }
            })
        return result