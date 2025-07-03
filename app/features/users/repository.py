from typing import Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.features.users.model import UserModel
from fastapi import Request

class UserRepository:
    def __init__(self, request: Request) -> None:
        self.users_collection = request.app.state.db['users']
    
    async def insert_one(self, user: dict[str, Any]):
        self.users_collection.insert_one(user)