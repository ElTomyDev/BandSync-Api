from fastapi import Request

from app.features.locations.model import LocationModel
from app.features.locations.repository import LocationRepository
from app.features.locations.schema import LocationUpdateSchema
from app.features.users.model import UserModel
from app.features.users.schema import UserFindSchema
from app.features.users.validations import UserValidations


class LocationService:
    def __init__(self, request: Request):
        self.__repository = LocationRepository(request)
        
    async def create_location_model(self) -> LocationModel:
        return LocationModel()

    async def update_location(self, user_find_schema: UserFindSchema, location_data: LocationUpdateSchema) -> None:
        UserValidations.valid_id_and_username_fields(user_find_schema)
        update_result = await self.__repository.update_one(user_find_schema.username, user_find_schema.id, location_data)
        UserValidations.valid_update_or_delete_result(update_result.matched_count, "An error occurred while trying to update the user's location")
    
    