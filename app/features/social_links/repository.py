from typing import Any
from bson import ObjectId
from fastapi import Request
from app.features.social_links.schema import SocialLinkResposeSchema
from app.features.social_links.model import SocialLinkModel

class SocialLinkRepository:
    def __init__(self, request: Request) -> None:
        self.social_collection = request.app.state.db['social_links']
    
    async def insert_one(self, social_link_dict: dict[str, Any]) -> None:
        await self.social_collection.insert_one(social_link_dict)
    
    async def find_one_by_id(self, id: str) -> SocialLinkModel | None:
        social_link = await self.social_collection.find_one({"_id": ObjectId(id)})
        if social_link:
            return SocialLinkModel(**social_link)
        return social_link
    
    async def update_one_by_id(self, id: str, field: str, value: str) -> bool | None:
        """
        Actualiza el documento que corresponde a la id (id), modifica el campo (field) al valor (value).
        Retorna si la actualizacion fue o no exitosa
        """
        if value != None:
            result = await self.social_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set":{field: value}})
        
        return result.modified_count > 0
        