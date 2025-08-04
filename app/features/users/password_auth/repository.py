from datetime import datetime, timezone
from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult

class PasswordAuthRepository:
    def __init__(self, request: Request):
        self.__user_collection = request.app.state.db['users']
    
    async def update_password(self, user_id: ObjectId, new_password: str) -> UpdateResult:
        result = await self.__user_collection.update_one(
            {"_id": user_id},
            {"$set": {"password_auth.password": new_password,
                      "password_auth.last_update": datetime.now(timezone.utc)}}
        )
        return result