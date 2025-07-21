from typing import Any
from app.features.locations.model import LocationModel
from app.features.users.model import UserModel

from app.features.locations.repository import LocationRepository
from app.features.users.repository import UserRepository

from app.features.social_links.service import SocialLinksService
from app.features.users.features.user_password.service import UserPasswordService

from app.features.users.mappers import UserMappers

from app.features.users.schema import UserRegisterSchema
from app.features.locations.schema import LocationResponseSchema, LocationUpdateSchema
from app.features.social_links.schema import SocialLinksUpdateSchema

from fastapi import HTTPException, Request

class UserService:
    def __init__(self, request: Request):
        self.__user_repository = UserRepository(request)
        self.__location_repository = LocationRepository(request)
        
        self.__social_links_service = SocialLinksService(request)
        self.__password_service = UserPasswordService(request)
    
    async def create_user_document(self, user_data: UserRegisterSchema) -> dict[str, Any]:
        user = UserModel(**user_data.model_dump())

        await self.__password_service.create_password_document(user, user_data.password)
        await self.__social_links_service.create_social_links_document(user)
        
        # Creo un modelo para la localidad del usuario
        location = LocationModel()
        user.location_id = location.id # Paso la id location correspondiente al nuevo usuario
        
        
        await self.__location_repository.insert_one(location.model_dump())
        await self.__user_repository.insert_one(user.model_dump())
        
        return UserMappers.model_to_schema(user).model_dump()
    
    async def find_user_document(self, id: str|None, username: str|None) -> UserModel:
        if id == None and username == None:
            raise HTTPException(status_code=403, detail=f"You must provide at least one field (id or username)")
        
        user = await self.__user_repository.find_one(id, username)
        if user == None:
            raise HTTPException(state_code=404, detail=f"The user with {f"id: '{id}'" if id != None else f"username: '{username}'"}. Not found")
        return user
        
    async def update_social_links(self, id: str|None, username: str|None, social_links_data: SocialLinksUpdateSchema) -> dict[str, str]:
        user = await self.find_user_document(id, username)
        social_links_update = self.__social_links_service.update_social_links_document(user, social_links_data)
        return social_links_update
    
    async def find_social_links(self, id: str|None, username: str|None) -> dict[str, str]:
        user = await self.find_user_document(id, username)
        social_links_find = await self.__social_links_service.find_social_links(user)
        return social_links_find
    
    async def update_location(self, id: str|None, username: str|None, location_data: LocationUpdateSchema) -> dict[str, Any]:
        if id or username: # Falta lanzar exepcion en caso de False
            user = await self.__user_repository.find_one(id, username)
            field_update_count = 0 # Representa la cantidad total de campos modificados
            location_id_match_flag = False
            if user: # Si existe el usuario
                for field, value in location_data.model_dump().items(): # Para cada (campo, valor) de social_data
                    update_result = await self.__location_repository.update_one_by_id(str(user.location_id), field, value) # Acualiza el documento
                    if update_result: # Si la modificacion fue exitosa
                        field_update_count += 1 # Suma la cantidad de campos modificados
                        location_id_match_flag = True
        
        return {'modified_fields': field_update_count,
                'location_id_match': location_id_match_flag}
    
    async def find_location(self, id: str|None, username: str|None) -> dict[str, str|None]:
        location = None
        if id or username:
            user = await self.__user_repository.find_one(id, username)
            if user:
                location = await self.__location_repository.find_one_by_id(str(user.location_id))
        if location:
            return LocationResponseSchema(**location.model_dump()).model_dump()
        return {'error': 'social link not found'}