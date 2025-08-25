from datetime import datetime, timedelta, timezone
import secrets
from typing import Tuple
from bson import ObjectId
from fastapi import Request

from app.features.users.model import UserModel
from pymongo.results import UpdateResult

class EmailAuthRepository:
    def __init__(self, request: Request):
        self.__users_collection = request.app.state.db['users']
    
    async def find_one_by_email(self, email: str) -> UserModel | None:
        user = await self.__users_collection.find_one({'email_auth.email': email})
        
        if user:
            return UserModel(**user)
        return None
    
    async def exist_email(self, email: str) -> bool:
        return await self.find_one_by_email(email) != None
    
    async def find_one_by_token(self, token: str) -> UserModel | None:
        user = await self.__users_collection.find_one({'email_auth.email_verification_token': token})
        if user:
            return UserModel(**user)
        return None
    
    async def generate_new_token(self, email: str) -> Tuple[UpdateResult, str|None]:
        token = secrets.token_urlsafe(32) 
        update_result = await self.__users_collection.update_one(
            {"email_auth.email": email},
            {"$set":{
                "email_auth.email_verification_token": token,
                "email_auth.email_verification_expiry": datetime.now(timezone.utc) + timedelta(hours=48)}
            }
        )
        token = token if update_result.matched_count != 0 else None
        return update_result, token
    
    async def mark_as_verified_by_id(self, user_id: ObjectId) -> UpdateResult:
        update_result = await self.__users_collection.update_one(
            {"_id": user_id},
            {"$set": {"email_auth.email_verified": True},
            "$unset": {"email_auth.email_verification_token": None,
                      "email_auth.email_verification_expiry": None}}
        )
        return update_result