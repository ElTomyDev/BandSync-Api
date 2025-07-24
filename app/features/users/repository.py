from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.features.users.model import UserModel
from fastapi import Request

class UserRepository:
    def __init__(self, request: Request) -> None:
        self.__users_collection = request.app.state.db['users']
    
    async def insert_one(self, user_dict: UserModel) -> None:
       await self.__users_collection.insert_one(user_dict.model_dump())
    
    async def find_one(self, id: str | None = None, username: str | None = None) -> UserModel | None:
        user = None
        if id:
            user = await self.__users_collection.find_one({'_id': ObjectId(id)})
        elif username:
            user = await self.__users_collection.find_one({'username': username})
        
        if user:
            return UserModel(**user)
        return user
            