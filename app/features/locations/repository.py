from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult

from app.features.locations.model import LocationModel
from app.features.locations.schema import LocationUpdateSchema

class LocationRepository:
    def __init__(self, request: Request) -> None:
        self.__users_collection = request.app.state.db['users']
    
    async def update_one(self, username: str, user_id: str, location_data: LocationUpdateSchema) -> UpdateResult:
        if username == None:
            result = await self.__users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set":{"location.country": location_data.country,
                        "location.state": location_data.state,
                        "location.city": location_data.city,
                        "location.postal_code": location_data.postal_code,
                        "location.address": location_data.address}})
            return result
        result = await self.__users_collection.update_one(
                {"username": username},
                {"$set":{"location.country": location_data.country,
                        "location.state": location_data.state,
                        "location.city": location_data.city,
                        "location.postal_code": location_data.postal_code,
                        "location.address": location_data.address}})
        return result