from typing import Any
from bson import ObjectId
from fastapi import Request

from app.features.locations.model import LocationModel

class LocationRepository:
    def __init__(self, request: Request) -> None:
        self.__locations_collection = request.app.state.db['locations']
    
    async def insert_one(self, location_dict: dict[str, Any]) -> None:
        await self.__locations_collection.insert_one(location_dict)
    
    async def find_one_by_id(self, id: str) -> LocationModel | None:
        location = await self.__locations_collection.find_one({"_id": ObjectId(id)})
        if location:
            return LocationModel(**location)
        return location
    
    async def update_one_by_id(self, id: str, field: str, value: str) -> bool | None:
        """
        Actualiza el documento que corresponde a la id (id), modifica el campo (field) al valor (value).
        Retorna si la actualizacion fue o no exitosa
        """
        modified_flag = False
        if value != None:
            result = await self.__locations_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set":{field: value}})
            modified_flag = result.modified_count > 0
        
        return modified_flag