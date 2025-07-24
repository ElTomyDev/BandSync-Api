from fastapi import HTTPException, Request

from app.features.social_links.model import SocialLinkModel
from app.features.social_links.repository import SocialLinksRepository
from app.features.social_links.schema import SocialLinksResponseSchema, SocialLinksUpdateSchema
from app.features.users.model import UserModel


class SocialLinksService:
    def __init__(self, request: Request):
        self.__repository = SocialLinksRepository(request)
    
    async def create_social_links_document(self, user: UserModel) -> None:
        if user == None: # Si el usuario no existe
            raise HTTPException(status_code=404, detail="Reference user not found")
        
        social_links = SocialLinkModel()
        await self.__repository.insert_one(social_links.model_dump())
        user.social_id = social_links.id
        
    async def update_social_links_document(self, user: UserModel, social_links_data: SocialLinksUpdateSchema)-> dict[str, int]:
        if user == None: # Si el usuario no existe
            raise HTTPException(status_code=404, detail="Reference user not found")
        if user.social_id == None:
            raise HTTPException(status_code=404, details=f"The user reference does not have a 'social_id' assigned")
        
        update_result = await self.__repository.update_one_by_id(user.social_id, social_links_data)
        return {'modified_fields': update_result.modified_count}
    
    async def find_social_links_document(self, user: UserModel) -> dict[str, str]:
        if user == None:
            raise HTTPException(status_code=404, detail="Reference user not found")
        if user.social_id == None:
            raise HTTPException(status_code=404, details=f"The user reference does not have a 'social_id' assigned")
        
        social_links = await self.__repository.find_one_by_id(user.social_id)
        if social_links == None:
            raise HTTPException(status_code=404, details=f"social_links with id '{user.social_id}' not found")
        
        return SocialLinksResponseSchema(**social_links.model_dump()).model_dump()