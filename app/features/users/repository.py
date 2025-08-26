from datetime import datetime, timedelta, timezone
from typing import Any
from bson import ObjectId
from app.features.users.model import UserModel
from fastapi import Request
from pymongo.results import DeleteResult, UpdateResult

class UserRepository:
    def __init__(self, request: Request) -> None:
        self.__users_collection = request.app.state.db['users']
    
    async def insert_one(self, user_dict: UserModel) -> None:
       await self.__users_collection.insert_one(user_dict.model_dump())
    
    async def find_one_by_id_or_username(self, id: str|None=None, username: str|None=None) -> UserModel | None:
        if id == None:
            user = await self.__users_collection.find_one({'username': username})
            if user:
                return UserModel(**user)
            return user
        user = await self.__users_collection.find_one({'_id': ObjectId(id)})
        if user:
            return UserModel(**user)
        return user
    
    async def find_one_by_username_or_email(self, username: str|None, email: str|None) -> UserModel | None:
        if username == None:
            user = await self.__users_collection.find_one({'email_auth.email': email})
            if user:
                return UserModel(**user)
            return user
        user = await self.__users_collection.find_one({'username': username})
        if user:
            return UserModel(**user)
        return user
        
    async def update_one(self, user_id: str|None, username: str|None, field:str, value: Any) -> UpdateResult:
        if user_id == None:
            update_result = await self.__users_collection.update_one(
                {"username": username},
                {"$set":{field:value}}
            )
            return update_result
        update_result = await self.__users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set":{field:value}}
        )
        return update_result
    
    async def exist_username(self, username: str|None=None)-> bool:
        return await self.find_one_by_id_or_username(None, username) != None
    
    async def delete_one(self, user_id: str|None=None, username: str|None=None) -> DeleteResult:
        if user_id == None:
            delete_result = await self.__users_collection.delete_one({'username': username})
            return delete_result
        delete_result = await self.__users_collection.delete_one({'_id': ObjectId(user_id)})
        return delete_result

    async def find_one_by_email(self, email: str) -> UserModel | None:
        user = await self.__users_collection.find_one({'email_auth.email': email})
        
        if user:
            return UserModel(**user)
        return None
    
    async def exist_email(self, email: str) -> bool:
        return await self.find_one_by_email(email) != None
    
    async def generate_new_token(self, token: str, email: str) -> UpdateResult: 
        update_result = await self.__users_collection.update_one(
            {"email_auth.email": email},
            {"$set":{
                "email_auth.email_verification_token_hash": token,
                "email_auth.email_verification_expiry": datetime.now(timezone.utc) + timedelta(hours=24)}
            }
        )
        return update_result
    
    async def mark_as_verified_by_id(self, user_id: ObjectId) -> UpdateResult:
        update_result = await self.__users_collection.update_one(
            {"_id": user_id},
            {"$set": {"email_auth.email_verified": True},
            "$unset": {"email_auth.email_verification_token_hash": None,
                      "email_auth.email_verification_expiry": None}}
        )
        return update_result

    async def update_password(self, user_id: ObjectId, new_password: str) -> UpdateResult:
        result = await self.__users_collection.update_one(
            {"_id": user_id},
            {"$set": {"password_auth.password": new_password,
                    "password_auth.last_update": datetime.now(timezone.utc)}}
        )
        return result