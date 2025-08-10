from app.features.locations.service import LocationService
from app.features.users.email_auth.service import EmailAuthService
from app.features.users.password_auth.schema import UpdatePasswordSchema
from app.features.users.password_auth.service import PasswordAuthService
from app.features.social_links.service import SocialLinksService

from app.features.users.model import UserModel
from app.features.users.repository import UserRepository
from app.features.users.validations import UserValidations
from app.features.users.mappers import UserMappers

from app.features.users.schema import UpdateDescriptionSchema, UpdateNameSchema, UpdatePhoneNumberSchema, UserFindSchema, UserRegisterSchema, UserResponseSchema
from app.features.locations.schema import LocationUpdateSchema
from app.features.social_links.schema import UpdateSocialLinksSchema

from fastapi import HTTPException, Request


class UserService:
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
        
        self.__social_links_service = SocialLinksService(request)
        self.__password_auth_service = PasswordAuthService(request)
        self.__location_service = LocationService(request)
        self.__email_auth_service = EmailAuthService(request)
    
    # -----------------------
    # --- PRIVATE METHODS ---
    # -----------------------
    async def __get_user_document(self, user_find_schema: UserFindSchema) -> UserModel:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        user = await self.__repository.find_one(user_find_schema.id, user_find_schema.username)
        UserValidations.valid_user_existence(user_find_schema, user)
        return user
    
    # ---------------------
    # --- OTHER METHODS ---
    # ---------------------
    async def create_user_document(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        UserValidations.valid_username_in_use(await self.__repository.exist_username(None, user_data.username), user_data.username)
        
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
    
    async def delete_user(self, user_find_schema: UserFindSchema) -> None:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        delete_result = await self.__repository.delete_one(user_find_schema.id, user_find_schema.username)
        UserValidations.valid_update_or_delete_result(delete_result.deleted_count, "User not found")
    
    # ----------------------
    # --- UPDATE METHODS ---
    # ----------------------
    async def update_user_description(self, user_find_schema: UserFindSchema, update_description_schema: UpdateDescriptionSchema) -> None:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        update_result = await self.__repository.update_one(
            user_find_schema.id,
            user_find_schema.username,
            "description",
            update_description_schema.new_description
        )
        UserValidations.valid_update_or_delete_result(
            update_result.matched_count, 
            "An error occurred while trying to update the user's description."
        )
    
    async def update_user_phone_number(self, user_find_schema: UserFindSchema, update_phone_number_schema: UpdatePhoneNumberSchema) -> None:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        update_result = await self.__repository.update_one(
            user_find_schema.id,
            user_find_schema.username,
            "phone_number",
            update_phone_number_schema.new_phone_number
        )
        UserValidations.valid_update_or_delete_result(
            update_result.matched_count, 
            "An error occurred while trying to update the user's phone number."
        )
    
    async def update_user_name(self, user_find_schema: UserFindSchema, update_name_schema: UpdateNameSchema) -> None:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        update_result = await self.__repository.update_one(
            user_find_schema.id,
            user_find_schema.username,
            "name",
            update_name_schema.new_name
        )
        UserValidations.valid_update_or_delete_result(
            update_result.matched_count, 
            "An error occurred while trying to update the user's name."
        )
    
    async def update_user_social_links(self, user_find_schema: UserFindSchema, social_links_data: UpdateSocialLinksSchema) -> None:
        user = await self.__get_user_document(user_find_schema)
        await self.__social_links_service.update_social_links(user, social_links_data)

    async def update_user_location(self, user_find_schema: UserFindSchema, location_data: LocationUpdateSchema) -> None:
        user = await self.__get_user_document(user_find_schema)
        await self.__location_service.update_location(user, location_data)
    
    async def update_user_password(self, user_find_schema: UserFindSchema, update_password_data: UpdatePasswordSchema) -> None:
        user = await self.__get_user_document(user_find_schema)
        await self.__password_auth_service.update_password(user, update_password_data.old_password, update_password_data.new_password)