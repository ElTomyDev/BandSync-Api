from bson import ObjectId
from app.features.users.model import UserModel
from fastapi import Request
from pymongo.results import DeleteResult
class UserRepository:
    def __init__(self, request: Request) -> None:
        self.__users_collection = request.app.state.db['users']
    
    async def insert_one(self, user_dict: UserModel) -> None:
       await self.__users_collection.insert_one(user_dict.model_dump())
    
    async def find_one(self, id: str|None=None, username: str|None=None) -> UserModel | None:
        user = None
        if id == None:
            user = await self.__users_collection.find_one({'username': username})
            if user:
                return UserModel(**user)
        user = await self.__users_collection.find_one({'_id': ObjectId(id)})
        
        if user:
            return UserModel(**user)
        return user
    
    async def delete_one(self, id: str|None=None, username: str|None=None) -> DeleteResult:
        if id == None:
            delete_result = await self.__users_collection.delete_one({'username': username})
            return delete_result
        delete_result = await self.__users_collection.delete_one({'_id': ObjectId(id)})
        return delete_result
