from fastapi import APIRouter, status, Depends, Request
from app.schemas.user_schemas import UserRegisterSchema, UserResponseSchema
from app.services.user_service import UserService
from app.db.database_provider import get_mongo_db
from motor.motor_asyncio import AsyncIOMotorDatabase

class UserRoute:
    def __init__(self) -> None:
        
        self.router = APIRouter(prefix="/users", tags=["Users"])
        
        # POST para registar un usuario
        self.router.post(
            "/register",
            response_model=UserResponseSchema,
            status_code=status.HTTP_201_CREATED,
        )(self.register_user)
    
    async def register_user(self, user: UserRegisterSchema, request: Request):
        user_service = UserService(request)
        new_user = await user_service.create_user(user)
        return new_user