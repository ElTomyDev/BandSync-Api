from app.features.users.model import UserModel
from app.features.users.schema import UserRegisterSchema, UserResponseSchema
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Request

class UserService:
    def __init__(self, request: Request):
        self.db: AsyncIOMotorDatabase = request.app.state.db
    
    async def create_user(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        user = UserModel(**user_data.model_dump()).model_dump()


        await self.db["users"].insert_one(user)
        return UserResponseSchema(**user)