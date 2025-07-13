from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.features.users.model import UserModel
from fastapi import Request

class UserRepository:
    def __init__(self, request: Request) -> None:
        self.users_collection = request.app.state.db['users']
    
    async def insert_one(self, user_dict: dict[str, Any]) -> None:
       await self.users_collection.insert_one(user_dict)
    
    async def find_one(self, id: ObjectId | None = None, username: str | None = None) -> UserModel | None:
        user = None
        if id:
            user = await self.users_collection.find_one({'_id': id})
        elif username:
            user = await self.users_collection.find_one({'username': username})
        
        if user:
            return UserModel(**user)
        return user
            