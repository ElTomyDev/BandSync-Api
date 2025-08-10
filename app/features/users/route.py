from typing import Annotated
from app.features.locations.schema import LocationUpdateSchema
from app.features.users.email_auth.service import EmailAuthService
from app.features.users.password_auth.schema import UpdatePasswordSchema
from app.features.users.schema import UserFindSchema, UserRegisterSchema, UserResponseSchema
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
            "/delete-user",
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
        
        # ROUTE FOR UPDATE USER PASSWORD
        self.router.put(
            "/update-user-password",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_password_route)
        
        # ROUTE FOR UPDATE SOCIAL LINKS
        self.router.put(
            "/update-user-social-links",
            status_code=status.HTTP_204_NO_CONTENT
        )(self.update_user_social_links_route)
        
        # ROUTE FOR UPDATE LOCATION
        self.router.put(
            "/update-user-location",
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