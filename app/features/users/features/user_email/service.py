from fastapi import Request

from app.features.users.features.user_email.model import UserEmailModel
from app.features.users.features.user_email.repository import UserEmailRepository
from app.features.users.model import UserModel


class UserEmailService:
    def __init__(self, request: Request):
        self.__repository = UserEmailRepository(request)
    
    async def create_email_document(self, user: UserModel, email: str) -> None:
        email_created = UserEmailModel(user_id=user.id, email=email)
        self.__repository.insert_one(email_created)