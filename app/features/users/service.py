from typing import Any
from bson import ObjectId
from app.features.locations.model import LocationModel
from app.features.locations.repository import LocationRepository
from app.features.locations.schema import LocationResponseSchema, LocationUpdateSchema
from app.features.users.model import UserModel
from app.features.users.mappers import UserMappers
from app.features.social_links.model import SocialLinkModel
from app.features.users.repository import UserRepository
from app.features.social_links.repository import SocialLinkRepository
from app.features.users.schema import UserRegisterSchema
from app.features.social_links.schema import SocialLinkResposeSchema, SocialLinkUpdateSchema
from fastapi import Request

class UserService:
    def __init__(self, request: Request):
        self.__user_repository = UserRepository(request)
        self.__social_link_repository = SocialLinkRepository(request)
        self.__location_repository = LocationRepository(request)
    
    async def create_user(self, user_data: UserRegisterSchema) -> dict[str, Any]:
        user = UserModel(**user_data.model_dump())
        
        # Creo un modelo para las redes sociales
        social = SocialLinkModel()
        
        # Creo un modelo para la localidad del usuario
        location = LocationModel()
        
        user.social_id = social.id # Paso la id social correspondiente al nuevo usuario
        user.location_id = location.id # Paso la id location correspondiente al nuevo usuario
        
        await self.__social_link_repository.insert_one(social.model_dump())
        await self.__location_repository.insert_one(location.model_dump())
        await self.__user_repository.insert_one(user.model_dump())
        
        return UserMappers.model_to_schema(user).model_dump()
    
    async def update_social_links(self, id: str|None, username: str|None, social_data: SocialLinkUpdateSchema) -> dict[str, Any]:
        if id or username: # Falta lanzar exepcion en caso de False
            user = await self.__user_repository.find_one(id, username)
            field_update_count = 0 # Representa la cantidad total de campos modificados
            social_id_match_flag = False
            if user: # Si existe el usuario
                for field, value in social_data.model_dump().items(): # Para cada (campo, valor) de social_data
                    update_result = await self.__social_link_repository.update_one_by_id(str(user.social_id), field, value) # Acualiza el documento
                    if update_result: # Si la modificacion fue exitosa
                        field_update_count += 1 # Suma la cantidad de campos modificados
                        social_id_match_flag = True
                
        return {'modified_fields': field_update_count,
                'social_id_match': social_id_match_flag}
    
    async def find_social_links(self, id: str|None, username: str|None) -> dict[str, str]:
        social_links = None
        if id or username:
            user = await self.__user_repository.find_one(id, username)
            if user:
                social_links = await self.__social_link_repository.find_one_by_id(str(user.social_id))
        if social_links:
            return SocialLinkResposeSchema(**social_links.model_dump()).model_dump()
        return {'error': 'social link not found'}
    
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