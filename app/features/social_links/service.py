from typing import Any
from fastapi import HTTPException, Request

from app.features.social_links.model import SocialLinksModel
from app.features.social_links.repository import SocialLinksRepository
from app.features.social_links.schema import SocialLinksResponseSchema, SocialLinksUpdateSchema
from app.features.users.model import UserModel


class SocialLinksService:
    def __init__(self, request: Request):
        self.__repository = SocialLinksRepository(request)
    
    async def create_social_links_document(self, user: UserModel) -> None:
        if user == None: # Si el usuario no existe
            raise HTTPException(status_code=404, detail="Reference user not found")
        
        social_links = SocialLinksModel()
        await self.__repository.insert_one(social_links)
        user.social_links = social_links.id
        
    async def update_social_links_document(self, user: UserModel, social_links_data: SocialLinksUpdateSchema) -> None:
        if user == None: # Si el usuario no existe
            raise HTTPException(status_code=404, detail="Reference user not found")
        if user.social_links == None:
            raise HTTPException(status_code=404, details=f"The user reference does not have a 'social_id' assigned")
        
        update_result = await self.__repository.update_one_by_id(user.social_links, social_links_data)
    
    async def find_social_links_document(self, user: UserModel) -> SocialLinksResponseSchema:
        if user == None:
            raise HTTPException(status_code=404, detail="Reference user not found")
        if user.social_links == None:
            raise HTTPException(status_code=404, details=f"The user reference does not have a 'social_id' assigned")
        
        social_links = await self.__repository.find_one_by_id(user.social_links)
        if social_links == None:
            raise HTTPException(status_code=404, details=f"social_links with id '{user.social_links}' not found")
        
        return SocialLinksResponseSchema(**social_links.model_dump())