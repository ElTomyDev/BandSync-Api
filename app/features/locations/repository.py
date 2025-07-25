from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult

from app.features.locations.model import LocationModel
from app.features.locations.schema import LocationUpdateSchema

class LocationRepository:
    def __init__(self, request: Request) -> None:
        self.__locations_collection = request.app.state.db['locations']
    
    async def insert_one(self, location_model: LocationModel) -> None:
        await self.__locations_collection.insert_one(location_model.model_dump())
    
    async def find_one_by_id(self, id: ObjectId) -> LocationModel | None:
        location = await self.__locations_collection.find_one({"_id": id})
        if location:
            return LocationModel(**location)
        return location
    
    async def update_one_by_id(self, id: ObjectId, location_data: LocationUpdateSchema) -> UpdateResult:
        result = await self.__locations_collection.update_one(
            {"_id": id},
            {"$set":{"country": location_data.country,
                    "state": location_data.state,
                    "city": location_data.city,
                    "postal_code": location_data.postal_code,
                    "address": location_data.address}})
        return result