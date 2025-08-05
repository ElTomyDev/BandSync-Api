from app.features.locations.service import LocationService
from app.features.users.email_auth.service import EmailAuthService
from app.features.users.password_auth.service import PasswordAuthService
from app.features.social_links.service import SocialLinksService

from app.features.users.model import UserModel
from app.features.users.repository import UserRepository
from app.features.users.validations import UserValidations
from app.features.users.mappers import UserMappers

from app.features.users.schema import UpdatePasswordSchema, UserFindSchema, UserRegisterSchema, UserResponseSchema
from app.features.locations.schema import LocationUpdateSchema
from app.features.social_links.schema import UpdateSocialLinksSchema

from fastapi import Request


class UserService:
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
        
        self.__social_links_service = SocialLinksService(request)
        self.__password_auth_service = PasswordAuthService(request)
        self.__location_service = LocationService(request)
        self.__email_auth_service = EmailAuthService(request)
    
    async def __find_user_document(self, user_find_schema: UserFindSchema) -> UserModel:
        UserValidations.valid_id_and_username(user_find_schema)
        user = await self.__repository.find_one(user_find_schema.id, user_find_schema.username)
        UserValidations.valid_user_existence(user_find_schema, user)
        return user
    
    async def create_user_document(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        social_links_model = await self.__social_links_service.create_social_links_model()
        location_model = await self.__location_service.create_location_model()
        password_auth_model = await self.__password_auth_service.create_password_model(user_data.password)
        email_auth_model = await self.__email_auth_service.create_email_model(user_data.email)
        
        user = UserModel(
            location=location_model,
            social_links=social_links_model,
            password_auth=password_auth_model,
            email_auth=email_auth_model,
            name=user_data.name,
            lastname=user_data.lastname,
            username=user_data.username,
            description=user_data.description)
        
        await self.__repository.insert_one(user)
        
        return UserMappers.model_to_schema(user)
    
    async def update_user_password(self, user_find_schema: UserFindSchema, update_password_data: UpdatePasswordSchema) -> None:
        user = await self.__find_user_document(user_find_schema)
        await self.__password_auth_service.update_password(user, update_password_data.old_password, update_password_data.new_password)
    
    async def update_user_social_links(self, user_find_schema: UserFindSchema, social_links_data: UpdateSocialLinksSchema) -> None:
        user = await self.__find_user_document(user_find_schema)
        await self.__social_links_service.update_social_links(user, social_links_data)

    async def update_user_location(self, user_find_schema: UserFindSchema, location_data: LocationUpdateSchema) -> None:
        user = await self.__find_user_document(user_find_schema)
        await self.__location_service.update_location(user, location_data)
    
