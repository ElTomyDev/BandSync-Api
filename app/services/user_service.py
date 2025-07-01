from app.models.user_models import UserModel
from app.schemas.user_schema import RegisterUserSchema
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import json_util

async def create_user(user_data: RegisterUserSchema, db: AsyncIOMotorDatabase) -> UserModel:
    user = UserModel(**user_data.model_dump())
    
    user_dict = user.model_dump(by_alias=True)

    await db["users"].insert_one(user_dict)

    return user