from app.features.users.schema import UserRegisterSchema, UserResponseSchema
from app.features.users.service import UserService
from fastapi import APIRouter, status, Request


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