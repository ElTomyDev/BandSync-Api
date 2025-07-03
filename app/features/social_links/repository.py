from typing import Any
from bson import ObjectId
from fastapi import Request
from app.features.social_links.schema import SocialLinkResposeSchema

class SocialLinkRepository:
    def __init__(self, request: Request) -> None:
        self.social_collection = request.app.state.db['social_links']
    
    async def insert_one(self, social_link_dict: dict[str, Any]) -> None:
        self.social_collection.insert_one(social_link_dict)
    
    async def find_one_by_id(self, id: str) -> dict[str, Any] | None:
        social_link = await self.social_collection.find_one({"_id": ObjectId(id)})
        return SocialLinkResposeSchema(**social_link).model_dump()
    
    async def update_one_by_id(self, id: str, field: str, value: str) -> dict[str, int] | None:
        """
        Actualiza el documento que corresponde a la id (id), modifica el campo (field) al valor (value).
        """
        result = await self.social_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set":{field, value}})
        
        return {"affected_documents": result.modified_count,
                "document_matches": result.matched_count}
        