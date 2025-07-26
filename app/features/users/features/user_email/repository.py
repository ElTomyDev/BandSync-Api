from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult
from app.features.users.features.user_email.model import UserEmailModel


class UserEmailRepository:
    def __init__(self, request: Request):
        self.__collection = request.app.state.db["user_emails"]
    
    async def insert_one(self, user_email_model: UserEmailModel) -> None:
        await self.__collection.insert_one(user_email_model.model_dump())
    
    async def find_one_by_user_id(self, user_id: ObjectId) -> UserEmailModel | None:
        email = await self.__collection.find_one({'user_id': user_id})
        
        if email:
            return UserEmailModel(**email)
        return None
    
    async def update_email_by_user_id(self, user_id: ObjectId, new_email: str) -> UpdateResult:
        result = await self.__collection.update_one(
            {"user_id": user_id},
            {"$set":{
                'email': new_email,
                }
            })
        return result
    
    async def update_verification_by_user_id(self, user_id: ObjectId) -> UpdateResult:
        result = await self.__collection.update_one(
            {"user_id": user_id},
            {"$set":{
                'email_verified': True,
                }
            })
        return result