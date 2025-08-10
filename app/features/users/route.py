from typing import Annotated
from app.features.locations.schema import LocationUpdateSchema
from app.features.users.email_auth.service import EmailAuthService
from app.features.users.password_auth.schema import UpdatePasswordSchema
from app.features.users.schema import UpdateDescriptionSchema, UpdateLastnameSchema, UpdateNameSchema, UpdatePhoneNumberSchema, UpdateUsernameSchema, UserFindSchema, UserRegisterSchema, UserResponseSchema
from app.features.social_links.schema import UpdateSocialLinksSchema
from app.features.users.service import UserService
from fastapi import APIRouter, Body, Depends, status, Request


class UserRoute:
    def __init__(self) -> None:
        
        self.router = APIRouter(prefix="/users", tags=["Users"])
        
        # ROUTE FOR REGISTER NEW USER
        self.router.post(
            "/register",
            response_model=UserResponseSchema,
            status_code=status.HTTP_201_CREATED,
        )(self.register_user)
        
        # ROUTE FOR DELETE USER
        self.router.delete(
            "/delete",
            status_code=status.HTTP_204_NO_CONTENT,
        )(self.delete_user)
        
        # ROUTE FOR VERIFY EMAIL
        self.router.get(
            "/verify-email",
            status_code=status.HTTP_202_ACCEPTED
        )(self.verify_email)
        
        # ROUTE FOR GENERATE NEW TOKEN
        self.router.get(
            "/generate-new-token",
            status_code=status.HTTP_202_ACCEPTED
        )(self.generate_new_email_token)
        
        # ROUTER FOR UPDATE USER DESCRIPTION
        self.router.put(
            "/update-description",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_description_route)
        
        # ROUTER FOR UPDATE USER PHONE NUMBER
        self.router.put(
            "/update-phone-number",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_phone_number_route)
        
        # ROUTER FOR UPDATE USER NAME
        self.router.put(
            "/update-name",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_name_route)
        
        # ROUTER FOR UPDATE USER LASTNAME
        self.router.put(
            "/update-lastname",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_lastname_route)
        
        # ROUTER FOR UPDATE USER USERNAME
        self.router.put(
            "/update-username",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_username_route)
        
        # ROUTE FOR UPDATE USER PASSWORD
        self.router.put(
            "/update-password",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_password_route)
        
        # ROUTE FOR UPDATE SOCIAL LINKS
        self.router.put(
            "/update-social-links",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_user_social_links_route)
        
        # ROUTE FOR UPDATE LOCATION
        self.router.put(
            "/update-location",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_user_location_route)
    
    # --------------------
    # --- USER METHODS ---
    # --------------------
    async def register_user(self, user: UserRegisterSchema, request: Request) -> UserResponseSchema:
        user_service = UserService(request)
        new_user = await user_service.create_user_document(user)
        return new_user
    
    async def delete_user(self, user_find_schema: Annotated[UserFindSchema, Depends()], request: Request) -> None:
        user_service = UserService(request)
        await user_service.delete_user(user_find_schema)
        
    async def update_description_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], update_description_schema: Annotated[UpdateDescriptionSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        await user_service.update_user_description(user_find_schema, update_description_schema)
    
    async def update_phone_number_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], update_phone_number_schema: Annotated[UpdatePhoneNumberSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        await user_service.update_user_phone_number(user_find_schema, update_phone_number_schema)
        
    async def update_name_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], update_name_schema: Annotated[UpdateNameSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        await user_service.update_user_name(user_find_schema, update_name_schema)
        
    async def update_lastname_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], update_lastname_schema: Annotated[UpdateLastnameSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        await user_service.update_user_lastname(user_find_schema, update_lastname_schema)
    
    async def update_username_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], update_username_schema: Annotated[UpdateUsernameSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        await user_service.update_user_username(user_find_schema, update_username_schema)
    
    # --------------------------
    # --- EMAIL AUTH METHODS ---
    # --------------------------
    async def verify_email(self, token: str, request: Request) -> None:
        email_auth_service = EmailAuthService(request)
        await email_auth_service.verify_email(token)
    
    async def generate_new_email_token(self, email: str, request: Request) -> None:
        email_auth_service = EmailAuthService(request)
        await email_auth_service.generate_new_verify_token(email)
    
    # -----------------------------
    # --- PASSWORD AUTH METHODS ---
    # -----------------------------
    async def update_password_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], update_password_data: Annotated[UpdatePasswordSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        await user_service.update_user_password(user_find_schema, update_password_data)
    
    # ----------------------------
    # --- SOCIAL LINKS METHODS ---
    # ----------------------------
    async def update_user_social_links_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], social_data: Annotated[UpdateSocialLinksSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        return await user_service.update_user_social_links(user_find_schema, social_data)
    
    # ------------------------
    # --- LOCATION METHODS ---
    # ------------------------
    async def update_user_location_route(self, user_find_schema: Annotated[UserFindSchema, Depends()], location_data: Annotated[LocationUpdateSchema, Body()], request: Request) -> None:
        user_service = UserService(request)
        return await user_service.update_user_location(user_find_schema, location_data)