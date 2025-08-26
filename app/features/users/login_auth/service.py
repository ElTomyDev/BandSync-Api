from fastapi import Request
from app.features.users.login_auth.model import LoginAuthModel
from app.features.users.repository import UserRepository


class LoginAuthService():
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
    
    async def create_login_model(self) -> LoginAuthModel:
        return LoginAuthModel()