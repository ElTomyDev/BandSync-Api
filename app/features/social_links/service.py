from fastapi import Request

from app.features.social_links.model import SocialLinksModel
from app.features.social_links.repository import SocialLinksRepository
from app.features.social_links.schema import UpdateSocialLinksSchema
from app.features.users.model import UserModel
from app.features.users.schema import UserFindSchema
from app.features.users.validations import UserValidations


class SocialLinksService:
    def __init__(self, request: Request):
        self.__repository = SocialLinksRepository(request)
    
    async def create_social_links_model(self) -> SocialLinksModel:
        return SocialLinksModel()
    
    async def update_social_links(self, user_find_schema: UserFindSchema, social_links_data: UpdateSocialLinksSchema) -> None:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        update_result = await self.__repository.update_one(user_find_schema.username, user_find_schema.id, social_links_data)
        UserValidations.valid_update_or_delete_result(update_result.matched_count, "An error occurred while trying to update the user's social links")