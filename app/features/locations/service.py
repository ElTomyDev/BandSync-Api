from fastapi import HTTPException, Request

from app.features.locations.model import LocationModel
from app.features.locations.repository import LocationRepository
from app.features.locations.schema import LocationResponseSchema, LocationUpdateSchema
from app.features.users.model import UserModel


class LocationService:
    def __init__(self, request: Request):
        self.__repository = LocationRepository(request)
        
    async def create_location_document(self, user: UserModel):
        if user == None: # Si el usuario no existe
            raise HTTPException(status_code=404, detail="Reference user not found")
        
        location = LocationModel()
        await self.__repository.insert_one(location)
        user.location_id = location.id

    async def update_location_document(self, user: UserModel, location_data: LocationUpdateSchema) -> None:
        if user == None: # Si el usuario no existe
            raise HTTPException(status_code=404, detail="Reference user not found")
        if user.location_id == None:
            raise HTTPException(status_code=404, details=f"The user reference does not have a 'location_id' assigned")
        
        update_result = await self.__repository.update_one_by_id(user.location_id, location_data)
    
    async def find_location_document(self, user: UserModel) -> LocationResponseSchema:
        if user == None:
            raise HTTPException(status_code=404, detail="Reference user not found")
        if user.location_id == None:
            raise HTTPException(status_code=404, details=f"The user reference does not have a 'location_id' assigned")
        
        location = await self.__repository.find_one_by_id(user.location_id)
        
        if location == None:
            raise HTTPException(status_code=404, details=f"location with id '{str(user.location_id)}' not found")
        return LocationResponseSchema(**location.model_dump())
        