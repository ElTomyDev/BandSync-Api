from app.features.users.model import UserModel
from app.features.social_links.model import SocialLinkModel
from app.features.users.repository import UserRepository
from app.features.social_links.repository import SocialLinkRepository
from app.features.users.schema import UserRegisterSchema, UserResponseSchema
from fastapi import Request

class UserService:
    def __init__(self, request: Request):
        self.user_repository = UserRepository(request)
        self.social_link_repository = SocialLinkRepository(request)
    
    async def create_user(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        user = UserModel(**user_data.model_dump()).model_dump()
        social_link = SocialLinkModel()
        user['id_social'] = social_link['id']
        await self.user_repository.insert_one(user)
        return UserResponseSchema(**user)