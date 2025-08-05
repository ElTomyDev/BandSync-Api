from fastapi import HTTPException, Request

from app.features.locations.model import LocationModel
from app.features.locations.repository import LocationRepository
from app.features.locations.schema import LocationResponseSchema, LocationUpdateSchema
from app.features.users.model import UserModel


class LocationService:
    def __init__(self, request: Request):
        self.__repository = LocationRepository(request)
        
    async def create_location_model(self) -> LocationModel:
        return LocationModel()

    async def update_location_document(self, user: UserModel, location_data: LocationUpdateSchema) -> None:
        update_result = await self.__repository.update_one_by_user_id(user.location, location_data)
    
    