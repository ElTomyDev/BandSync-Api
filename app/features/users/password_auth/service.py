from fastapi import Request
from passlib.hash import bcrypt

from app.features.users.password_auth.model import PasswordAuthModel
from app.features.users.password_auth.schema import UpdatePasswordSchema
from app.features.users.repository import UserRepository
from app.features.users.schema import UserFindSchema
from app.features.users.validations import UserValidations

class PasswordAuthService:
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
        
    async def create_password_model(self, password: str) -> PasswordAuthModel:
        user_password = PasswordAuthModel(
            password = bcrypt.hash(password)
        )
        return user_password
    
    async def update_password(self, user_find_schema: UserFindSchema, update_password_schema: UpdatePasswordSchema) -> None:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        user_model = await self.__repository.find_one_by_id_or_username(user_find_schema.id, user_find_schema.username)
        UserValidations.valid_user_not_found(user_find_schema, user_model)
        UserValidations.valid_password(update_password_schema.old_password, user_model.password_auth.password)
        
        update_result = await self.__repository.update_password(user_model.id, bcrypt.hash(update_password_schema.new_password))
        UserValidations.valid_update_or_delete_result(update_result.matched_count, "The password could not be updated")