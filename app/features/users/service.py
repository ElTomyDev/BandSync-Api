from bson import ObjectId
from app.features.users.model import UserModel
from app.features.social_links.model import SocialLinkModel
from app.features.users.repository import UserRepository
from app.features.social_links.repository import SocialLinkRepository
from app.features.users.schema import UserRegisterSchema, UserResponseSchema
from app.features.social_links.schema import SocialLinkUpdateSchema, SocialLinkResposeSchema
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
        
        return UserResponseSchema(**user.model_dump())
    
    async def update_social_links(self, username: str, social_data: SocialLinkUpdateSchema) -> dict[str, int]:
        user = self.user_repository.find_one(username=username)
        field_update_count = 0 # Representa la cantidad total de campos modificados
        
        if user: # Si existe el usuario
            for field, value in social_data.model_dump(): # Para cada (campo, valor) de social_data
                update_result = await self.social_link_repository.update_one_by_id(user.social_id, field, value) # Acualiza el documento
                if update_result: # Si la modificacion fue exitosa
                    field_update_count += 1 # Suma la cantidad de campos modificados
                
        return {'modified_fields': field_update_count}