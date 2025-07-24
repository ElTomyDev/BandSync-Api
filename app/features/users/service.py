from typing import Any
from app.features.locations.model import LocationModel
from app.features.locations.service import LocationService
from app.features.users.model import UserModel

from app.features.locations.repository import LocationRepository
from app.features.users.repository import UserRepository

from app.features.social_links.service import SocialLinksService
from app.features.users.features.user_password.service import UserPasswordService

from app.features.users.mappers import UserMappers

from app.features.users.schema import UserRegisterSchema, UserResponseSchema
from app.features.locations.schema import LocationResponseSchema, LocationUpdateSchema
from app.features.social_links.schema import SocialLinksResponseSchema, SocialLinksUpdateSchema

from fastapi import HTTPException, Request

class UserService:
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
        
        self.__social_links_service = SocialLinksService(request)
        self.__password_service = UserPasswordService(request)
        self.__location_service = LocationService(request)
    
    async def create_user_document(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        user = UserModel(**user_data.model_dump())

        await self.__password_service.create_password_document(user, user_data.password)
        await self.__social_links_service.create_social_links_document(user)
        await self.__location_service.create_location_document(user)
        
        await self.__repository.insert_one(user)
        
        return UserMappers.model_to_schema(user)
    
    async def find_user_document(self, id: str|None, username: str|None) -> UserModel:
        if id == None and username == None:
            raise HTTPException(status_code=403, detail=f"You must provide at least one field (id or username)")
        
        user = await self.__repository.find_one(id, username)
        if user == None:
            raise HTTPException(state_code=404, detail=f"The user with {f"id: '{id}'" if id != None else f"username: '{username}'"}. Not found")
        return user
        
    async def update_social_links_from_user(self, id: str|None, username: str|None, social_links_data: SocialLinksUpdateSchema) -> None:
        user = await self.find_user_document(id, username)
        await self.__social_links_service.update_social_links_document(user, social_links_data)
    
    async def find_social_links_from_user(self, id: str|None, username: str|None) -> SocialLinksResponseSchema:
        user = await self.find_user_document(id, username)
        social_links_find = await self.__social_links_service.find_social_links_document(user)
        return social_links_find
    
    async def update_location_from_user(self, id: str|None, username: str|None, location_data: LocationUpdateSchema) -> dict[str, int]:
        user = await self.find_user_document(id, username)
        location_update_result = await self.__location_service.update_location_document(user, location_data)
        return location_update_result
    
    async def find_location_from_user(self, id: str|None, username: str|None) -> dict[str, str|None]:
        user = await self.find_user_document(id, username)
        location_find = await self.__location_service.find_location_document(user)
        return location_find