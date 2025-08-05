from fastapi import Request

from app.features.social_links.model import SocialLinksModel
from app.features.social_links.repository import SocialLinksRepository
from app.features.social_links.schema import UpdateSocialLinksSchema
from app.features.users.model import UserModel


class SocialLinksService:
    def __init__(self, request: Request):
        self.__repository = SocialLinksRepository(request)
    
    async def create_social_links_model(self) -> SocialLinksModel:
        return SocialLinksModel()
    
    async def update_social_links(self, user: UserModel, social_links_data: UpdateSocialLinksSchema) -> None:
        update_result = await self.__repository.update_one_by_user_id(user.id, social_links_data)
    