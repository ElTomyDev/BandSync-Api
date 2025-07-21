from typing import Any
from app.features.locations.schema import LocationUpdateSchema
from app.features.users.schema import UserRegisterSchema, UserResponseSchema
from app.features.social_links.schema import SocialLinksUpdateSchema
from app.features.users.service import UserService
from fastapi import APIRouter, status, Request


class UserRoute:
    def __init__(self) -> None:
        
        self.router = APIRouter(prefix="/users", tags=["Users"])
        
        # POST para registar un usuario
        self.router.post(
            "/register",
            status_code=status.HTTP_201_CREATED,
        )(self.register_user)
        
        self.router.put(
            "/update-social-links-by-username",
            status_code=status.HTTP_200_OK
        )(self.update_user_social_links_by_username)
        
        self.router.put(
            "/update-social-links-by-id",
            status_code=status.HTTP_200_OK
        )(self.update_user_social_links_by_id)
        
        self.router.get(
            "/find-social-links-by-username",
            status_code=status.HTTP_200_OK
        )(self.find_user_social_links_by_username)
        
        self.router.get(
            "/find-social-links-by-id",
            status_code=status.HTTP_200_OK
        )(self.find_user_social_links_by_id)
        
        # Location
        self.router.put(
            "/update-location-by-username",
            status_code=status.HTTP_200_OK
        )(self.update_user_location_by_username)
        
        self.router.put(
            "/update-location-by-id",
            status_code=status.HTTP_200_OK
        )(self.update_user_location_by_id)
        
        self.router.get(
            "/find-location-by-username",
            status_code=status.HTTP_200_OK
        )(self.find_user_location_by_username)
        
        self.router.get(
            "/find-location-by-id",
            status_code=status.HTTP_200_OK
        )(self.find_user_location_by_id)
    
    async def register_user(self, user: UserRegisterSchema, request: Request) -> dict[str, Any]:
        user_service = UserService(request)
        new_user = await user_service.create_user_document(user)
        return new_user
    
    async def update_user_social_links_by_username(self, username: str, social_data: SocialLinksUpdateSchema, request: Request) -> dict[str, Any]:
        user_service = UserService(request)
        return await user_service.update_social_links(None, username, social_data)
    
    async def update_user_social_links_by_id(self, id: str, social_data: SocialLinksUpdateSchema, request: Request) -> dict[str, Any]:
        user_service = UserService(request)
        return await user_service.update_social_links(id, None, social_data)
    
    async def find_user_social_links_by_username(self, username: str, request: Request) -> dict[str, str|None]:
        user_service = UserService(request)
        return await user_service.find_social_links(None, username)
    
    async def find_user_social_links_by_id(self, id: str, request: Request) -> dict[str, str|None]:
        user_service = UserService(request)
        return await user_service.find_social_links(id, None)
    
    async def update_user_location_by_username(self, username: str, location_data: LocationUpdateSchema, request: Request) -> dict[str, Any]:
        user_service = UserService(request)
        return await user_service.update_location(None, username, location_data)
    
    async def update_user_location_by_id(self, id: str, location_data: LocationUpdateSchema, request: Request) -> dict[str, Any]:
        user_service = UserService(request)
        return await user_service.update_location(id, None, location_data)
    
    async def find_user_location_by_username(self, username: str, request: Request) -> dict[str, str|None]:
        user_service = UserService(request)
        return await user_service.find_location(None, username)
    
    async def find_user_location_by_id(self, id: str, request: Request) -> dict[str, str|None]:
        user_service = UserService(request)
        return await user_service.find_location(id, None)