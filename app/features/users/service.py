from bson import ObjectId
from app.features.users.model import UserModel
from app.features.users.mappers import UserMappers
from app.features.social_links.model import SocialLinkModel
from app.features.users.repository import UserRepository
from app.features.social_links.repository import SocialLinkRepository
from app.features.users.schema import UserRegisterSchema, UserResponseSchema
from app.features.social_links.schema import SocialLinkUpdateSchema
from fastapi import Request

class UserService:
    def __init__(self, request: Request):
        self.user_repository = UserRepository(request)
        self.social_link_repository = SocialLinkRepository(request)
    
    async def create_user(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        user = UserModel(**user_data.model_dump())
        
        # Creo un modelo para las redes sociales
        social = SocialLinkModel()
        
        user.social_id = social.id # Paso la id social correspondiente al nuevo usuario
        
        await self.social_link_repository.insert_one(social.model_dump())
        await self.user_repository.insert_one(user.model_dump())
        
        return UserMappers.model_to_schema(user)
    
    async def update_social_links(self, username: str, social_data: SocialLinkUpdateSchema) -> dict[str, int]:
        user = await self.user_repository.find_one(username=username)
        field_update_count = 0 # Representa la cantidad total de campos modificados
        
        if user: # Si existe el usuario
            print(user.social_id)
            for field, value in social_data.model_dump().items(): # Para cada (campo, valor) de social_data
                update_result = await self.social_link_repository.update_one_by_id(user.social_id, field, value) # Acualiza el documento
                if update_result: # Si la modificacion fue exitosa
                    field_update_count += 1 # Suma la cantidad de campos modificados
                
        return {'modified_fields': field_update_count}