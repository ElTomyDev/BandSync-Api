from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from app.features.locations.schema import LocationUpdateSchema
from app.features.locations.service import LocationService
from app.features.social_links.service import SocialLinksService
from app.features.users.email_auth.service import EmailAuthService
from app.features.users.login_auth.schema import LoginSchema, LoginTokenSchema
from app.features.users.login_auth.service import LoginAuthService
from app.features.users.model import UserModel
from app.features.users.password_auth.schema import UpdatePasswordSchema
from app.features.users.password_auth.service import PasswordAuthService
from app.features.users.schema import UpdateAccountStateSchema, UpdateDescriptionSchema, UpdateFindBandsSchema, UpdateImageURLSchema, UpdateLastnameSchema, UpdateMusicalRoleSchema, UpdateNameSchema, UpdatePhoneNumberSchema, UpdateUsernameSchema, UserFindSchema, UserRegisterSchema, UserResponseSchema
from app.features.social_links.schema import UpdateSocialLinksSchema
from app.features.users.service import UserService
from fastapi import APIRouter, Body, Depends, status, Request

user_router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth/login")

# -------------------------
# --- USER AUTH METHODS ---
# -------------------------
# ROUTES AUTH AND LOGIN
@user_router.post("/auth/login", response_model=LoginTokenSchema, status_code=status.HTTP_200_OK)
async def login(request: Request, login_schema: Annotated[LoginSchema, Depends()]) -> LoginTokenSchema:
    login_auth_service = LoginAuthService(request)
    return await login_auth_service.login(login_schema)

@user_router.get("/auth/me", status_code=status.HTTP_200_OK)
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> UserResponseSchema:
    login_auth_service = LoginAuthService(request)
    return await login_auth_service.get_current_user(token)

# --------------------
# --- USER METHODS ---
# --------------------
# ROUTE FOR REGISTER NEW USER
@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, user: UserRegisterSchema) -> UserResponseSchema:
    user_service = UserService(request)
    new_user = await user_service.create_user_document(user)
    return new_user

# ROUTE FOR DELETE USER
@user_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request, user_find_schema: Annotated[UserFindSchema, Depends()]) -> None:
    user_service = UserService(request)
    await user_service.delete_user(user_find_schema)

# ROUTER FOR UPDATE USER DESCRIPTION
@user_router.put("/update-description", status_code=status.HTTP_204_NO_CONTENT)
async def update_description_route(
    request: Request,
    update_description_schema: Annotated[UpdateDescriptionSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:

    user_service = UserService(request)
    await user_service.update_user(current_user.id, "description", update_description_schema.new_description)

# ROUTER FOR UPDATE USER PHONE NUMBER
@user_router.put("/update-phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number_route(
    request: Request,
    update_phone_number_schema: Annotated[UpdatePhoneNumberSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user(current_user.id, "phone_number", update_phone_number_schema.new_phone_number)

# ROUTER FOR UPDATE USER NAME
@user_router.put("/update-name", status_code=status.HTTP_204_NO_CONTENT)
async def update_name_route(
    request: Request,
    update_name_schema: Annotated[UpdateNameSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user(current_user.id, "name", update_name_schema.new_name)

# ROUTER FOR UPDATE USER LASTNAME
@user_router.put("/update-lastname", status_code=status.HTTP_204_NO_CONTENT)
async def update_lastname_route(
    request: Request,
    update_lastname_schema: Annotated[UpdateLastnameSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user(current_user.id, "lastname", update_lastname_schema.new_lastname)

# ROUTER FOR UPDATE USER USERNAME
@user_router.put("/update-username", status_code=status.HTTP_204_NO_CONTENT)
async def update_username_route(
    request: Request,
    update_username_schema: Annotated[UpdateUsernameSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user(current_user.id, "username", update_username_schema.new_username)

# ROUTER FOR UPDATE USER IMAGE URL
@user_router.put("/update-image-url", status_code=status.HTTP_204_NO_CONTENT)
async def update_imageurl_route(
    request: Request,
    update_imageurl_schema: Annotated[UpdateImageURLSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user_fields(current_user.id, "image_url", update_imageurl_schema.new_image_url)

# ROUTER FOR UPDATE USER FIND BANDS
@user_router.put("/update-find-bands", status_code=status.HTTP_204_NO_CONTENT)
async def update_find_bands_route(
    request: Request,
    update_find_bands_schema: Annotated[UpdateFindBandsSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user(current_user.id, "find_bands", update_find_bands_schema.find_bands)

# ROUTER FOR UPDATE USER MUSICAL ROLE
@user_router.put("/update-musical-role", status_code=status.HTTP_204_NO_CONTENT)
async def update_musical_role_route(
    request: Request,
    update_musical_role_schema: Annotated[UpdateMusicalRoleSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user(current_user.id, "musical_role", update_musical_role_schema.musical_role)

# ROUTER FOR UPDATE USER ACCOUNT STATE
@user_router.put("/update-account-state", status_code=status.HTTP_204_NO_CONTENT)
async def update_account_state_route(
    request: Request,
    update_account_state_schema: Annotated[UpdateAccountStateSchema, Body()],
    current_user: UserResponseSchema=Depends(get_current_user)) -> None:
    
    user_service = UserService(request)
    await user_service.update_user(current_user.id, "account_state", update_account_state_schema.account_state)

# --------------------------
# --- EMAIL AUTH METHODS ---
# --------------------------
# ROUTE FOR VERIFY EMAIL
@user_router.get("/verify-email",status_code=status.HTTP_202_ACCEPTED)
async def verify_email(request: Request, email: str, token: str) -> None:
    email_auth_service = EmailAuthService(request)
    await email_auth_service.verify_email(email, token)

# ROUTE FOR GENERATE NEW TOKEN
@user_router.get("/generate-new-token",status_code=status.HTTP_202_ACCEPTED)
async def generate_new_email_token(request: Request, email: str) -> None:
    email_auth_service = EmailAuthService(request)
    await email_auth_service.generate_new_verify_token(email)

# -----------------------------
# --- PASSWORD AUTH METHODS ---
# -----------------------------
# ROUTE FOR UPDATE USER PASSWORD
@user_router.put("/update-password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password_route(user_find_schema: Annotated[UserFindSchema, Depends()], update_password_schema: Annotated[UpdatePasswordSchema, Body()], request: Request) -> None:
    password_auth_service = PasswordAuthService(request)
    await password_auth_service.update_password(user_find_schema, update_password_schema)

# ----------------------------
# --- SOCIAL LINKS METHODS ---
# ----------------------------
# ROUTE FOR UPDATE SOCIAL LINKS
@user_router.put("/update-social-links", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_social_links_route(user_find_schema: Annotated[UserFindSchema, Depends()], social_data: Annotated[UpdateSocialLinksSchema, Body()], request: Request) -> None:
    social_links_service = SocialLinksService(request)
    return await social_links_service.update_social_links(user_find_schema, social_data)

# ------------------------
# --- LOCATION METHODS ---
# ------------------------
# ROUTE FOR UPDATE LOCATION
@user_router.put("/update-location", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_location_route(user_find_schema: Annotated[UserFindSchema, Depends()], location_data: Annotated[LocationUpdateSchema, Body()], request: Request) -> None:
    location_service = LocationService(request)
    return await location_service.update_location(user_find_schema, location_data)

