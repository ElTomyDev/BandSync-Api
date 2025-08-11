from fastapi import Request
from app.features.users.login_auth.model import LoginAuthModel


class LoginAuthService():
    def __init__(self, request: Request):
        pass
    
    async def create_login_model() -> LoginAuthModel:
        return LoginAuthModel()