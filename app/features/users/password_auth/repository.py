from datetime import datetime, timezone
from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult

from app.features.users.model import UserModel

class PasswordAuthRepository:
    def __init__(self, request: Request):
        self.__users_collection = request.app.state.db['users']
    
    async def find_one(self, id: str|None=None, username: str|None=None) -> UserModel | None:
        if id == None:
            user = await self.__users_collection.find_one({'username': username})
            if user:
                return UserModel(**user)
        user = await self.__users_collection.find_one({'_id': ObjectId(id)})
        if user:
            return UserModel(**user)
        return user
    
    async def update_password(self, username: str, user_id: str, new_password: str) -> UpdateResult:
        if username == None:
            result = await self.__users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password_auth.password": new_password,
                        "password_auth.last_update": datetime.now(timezone.utc)}}
            )
            return result
        result = await self.__users_collection.update_one(
                {"username": username},
                {"$set": {"password_auth.password": new_password,
                        "password_auth.last_update": datetime.now(timezone.utc)}}
            )
        return result

    
        