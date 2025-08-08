from datetime import datetime, timezone
from fastapi import HTTPException
from app.configs.send_email_config import NEW_TOKEN_URL_BASE
from app.features.users.model import UserModel
from app.features.users.schema import UserFindSchema


class UserValidations:
    def valid_id_and_username(user_find_schema: UserFindSchema) -> None:
        """
        Validates that at least one identifier (either `id` or `username`) is provided in the `user_find_schema`.

        Both fields are obtained from `UserFindSchema`, and the function ensures that they are not `None` simultaneously.
        If both are `None`, an HTTP 403 (Forbidden) exception is raised to prevent unauthorized access without sufficient user identification.
        
        Raises:
            `HTTPException`: If `id` and `username` is `None`, with status code 403 and a descriptive message. 
        """
        if user_find_schema.id == None and user_find_schema.username == None:
            raise HTTPException(status_code=403, detail=f"You must provide at least one field (id or username)")
    
    def valid_user_existence(user_find_schema: UserFindSchema, user: UserModel) -> None:
        """
        The function receives a `user_find_schema` with either an `id` or `username`, and a `user` object from a database query.
        If `user` is `None`, it raises an HTTP 404 exception indicating the user was not found.

        Raises:
            `HTTPException`: If `user` is `None`, with status code 404 and a descriptive message. 
        """
        if user == None:
            raise HTTPException(
                status_code=404, 
                detail=f"The user with {f"id: '{user_find_schema.id}'" if user_find_schema.id != None else f"username: '{user_find_schema.username}'"}. Not found")
    
    def valid_username_in_use(exist_user: bool, username: str) -> None:
        if exist_user:
            raise HTTPException(status_code=409, detail=f"The username '{username}' is already in use.")
    
    def valid_email_in_use(exist_user: bool, email: str) -> None:
        if exist_user:
            raise HTTPException(status_code=409, detail=f"The email '{email}' is already register.")
    
    def valid_email_is_already_verify(user_model:  UserModel) -> None:
        if user_model == None:
            raise HTTPException(status_code=409, detail="The email it is already verified")
    
    async def valid_email_expiry(expiry_date: datetime, email: str) -> None:
        if expiry_date is None or expiry_date.tzinfo is None:
            expiry_date = expiry_date.replace(tzinfo=timezone.utc)
            
        if expiry_date < datetime.now(timezone.utc):
            
            raise HTTPException(status_code=401, detail=f"The token is expired. Click here to generate a new token: {NEW_TOKEN_URL_BASE}/?email={email}")