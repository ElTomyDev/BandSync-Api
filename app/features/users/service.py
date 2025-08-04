from typing import Any
from app.features.locations.model import LocationModel
from app.features.locations.service import LocationService
from app.features.social_links.model import SocialLinksModel


from app.features.users.email_auth.service import EmailAuthService
from app.features.users.model import UserModel

from app.features.users.password_auth.service import PasswordAuthService
from app.features.users.repository import UserRepository

from app.features.social_links.service import SocialLinksService

from app.features.users.mappers import UserMappers

from app.features.users.schema import UpdatePasswordSchema, UserRegisterSchema, UserResponseSchema
from app.features.locations.schema import LocationResponseSchema, LocationUpdateSchema
from app.features.social_links.schema import SocialLinksResponseSchema, SocialLinksUpdateSchema

from fastapi import HTTPException, Request

class UserService:
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
        
        self.__social_links_service = SocialLinksService(request)
        self.__password_auth_service = PasswordAuthService(request)
        self.__location_service = LocationService(request)
        self.__email_auth_service = EmailAuthService()
    
    async def __find_user_document(self, id: str|None, username: str|None) -> UserModel:
        if id == None and username == None:
            raise HTTPException(status_code=403, detail=f"You must provide at least one field (id or username)")
        
        user = await self.__repository.find_one(id, username)
        if user == None:
            raise HTTPException(state_code=404, detail=f"The user with {f"id: '{id}'" if id != None else f"username: '{username}'"}. Not found")
        return user
    
    async def create_user_document(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        location = LocationModel()
        social_links = SocialLinksModel()
        
        password_auth_dict = await self.__password_auth_service.create_password_dict(user_data.password)
        email_auth_dict = await self.__email_auth_service.create_email_dict(user_data.email)
        
        user = UserModel(
            location=location,
            social_links=social_links,
            password_auth=password_auth_dict,
            email_auth=email_auth_dict,
            name=user_data.name,
            lastname=user_data.lastname,
            username=user_data.username,
            description=user_data.description)
        
        await self.__repository.insert_one(user)
        
        return UserMappers.model_to_schema(user)
    
    async def update_user_password(self, id:str|None, username: str|None, update_password_data: UpdatePasswordSchema) -> None:
        user = await self.__find_user_document(id, username)
        await self.__password_auth_service.update_password(user, update_password_data.old_password, update_password_data.new_password)
    
    async def verify_email(self, token: str) -> None:
        await self.__email_auth_service.verify_email(token)
    
    async def update_social_links_from_user(self, id: str|None, username: str|None, social_links_data: SocialLinksUpdateSchema) -> None:
        user = await self.__find_user_document(id, username)
        await self.__social_links_service.update_social_links_document(user, social_links_data)
    
    async def find_social_links_from_user(self, id: str|None, username: str|None) -> SocialLinksResponseSchema:
        user = await self.__find_user_document(id, username)
        social_links_find = await self.__social_links_service.find_social_links_document(user)
        return social_links_find
    
    async def update_location_from_user(self, id: str|None, username: str|None, location_data: LocationUpdateSchema) -> None:
        user = await self.__find_user_document(id, username)
        await self.__location_service.update_location_document(user, location_data)
    
    async def find_location_from_user(self, id: str|None, username: str|None) -> LocationResponseSchema:
        user = await self.__find_user_document(id, username)
        location_find = await self.__location_service.find_location_document(user)
        return location_find
    
    