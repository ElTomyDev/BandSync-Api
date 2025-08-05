from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult

from app.features.locations.model import LocationModel
from app.features.locations.schema import LocationUpdateSchema

class LocationRepository:
    def __init__(self, request: Request) -> None:
        self.__users_collection = request.app.state.db['users']
    
    async def update_one_by_user_id(self, user_id: ObjectId, location_data: LocationUpdateSchema) -> UpdateResult:
        result = await self.__users_collection.update_one(
            {"_id": user_id},
            {"$set":{"location.country": location_data.country,
                    "location.state": location_data.state,
                    "location.city": location_data.city,
                    "location.postal_code": location_data.postal_code,
                    "location.address": location_data.address}})
        return result