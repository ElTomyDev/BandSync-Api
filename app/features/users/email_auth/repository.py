from bson import ObjectId
from fastapi import Request

from app.features.users.model import UserModel
from pymongo.results import UpdateResult

class EmailAuthRepository:
    def __init__(self, request: Request):
        self.__user_collection = request.app.state.db['users']
    
    async def find_one_by_token(self, token: str) -> UserModel | None:
        user = await self.__user_collection.find_one({'email_auth.email_verification_token': token})
        if user:
            return UserModel(**user)
        return None
    
    async def mark_as_verified_by_id(self, user_id: ObjectId) -> UpdateResult:
        update_result = await self.__user_collection.update_one(
            {"_id": user_id},
            {"$set": {"email_auth.email_verified": True},
            "$unset": {"email_auth.email_verification_token": None,
                      "email_auth.email_verification_expiry": None}}
        )
        return update_result