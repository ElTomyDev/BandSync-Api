from app.models.user_models import UserModel
from app.schemas.user_schemas import RegisterUserSchema
from motor.motor_asyncio import AsyncIOMotorDatabase

async def create_user(user_data: RegisterUserSchema, db: AsyncIOMotorDatabase) -> UserModel:
    user = UserModel(**user_data.model_dump()).model_dump()

    await db["users"].insert_one(user)

    return user