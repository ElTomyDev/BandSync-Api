from datetime import datetime, timedelta, timezone
from passlib.hash import bcrypt
from fastapi import Depends, HTTPException, Request
from app.configs.login_config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_KEY
from app.features.users.login_auth.model import LoginAuthModel
from app.features.users.login_auth.schema import LoginSchema, LoginTokenSchema
from app.features.users.mappers import UserMappers
from app.features.users.repository import UserRepository
from app.features.users.schema import UserResponseSchema
from app.features.users.validations import UserValidations
from jose import ExpiredSignatureError, jwt, JWTError

class LoginAuthService():
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
    
    async def create_login_model(self) -> LoginAuthModel:
        return LoginAuthModel()
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_KEY, algorithm=ALGORITHM)
    
    async def login(self, login_schema: LoginSchema) -> LoginTokenSchema:
        UserValidations.valid_login_fields(login_schema)
        user = await self.__repository.find_one_by_username_or_email(login_schema.username, login_schema.email)
        
        UserValidations.valid_user_not_found(None, user, "The username or email is incorrect")
        if not bcrypt.verify(login_schema.password, user.password_auth.password):
            await self.__repository.update_login_failure(str(user.id), user.login_auth.failed_login_attempts)
            raise HTTPException(status_code=401, detail="Password incorrect")
        
        UserValidations.check_account_state(user.account_state)
        
        # reset attemps and update last conection
        await self.__repository.update_correct_login(str(user.id))
        
        # Create access token and return
        access_token = self.create_access_token(data={"sub": str(user.id)})
        return LoginTokenSchema(access_token=access_token)
        
    async def get_current_user(self, token: str) -> UserResponseSchema:
        try:
            payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
            UserValidations.valid_token_sub_not_found(str(payload.get("sub")))
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        
        
        user = await self.__repository.find_one_by_id_or_username(str(payload.get("sub")), None)
        UserValidations.valid_user_not_found(None, user)

        UserValidations.check_account_state(user.account_state)

        return UserMappers.model_to_schema(user)