from typing import Any
from bson import ObjectId
from fastapi import Request
from app.features.social_links.schema import SocialLinksResponseSchema, SocialLinksUpdateSchema
from app.features.social_links.model import SocialLinkModel
from pymongo.results import UpdateResult

class SocialLinksRepository:
    def __init__(self, request: Request) -> None:
        self.social_collection = request.app.state.db['social_links']
    
    async def insert_one(self, social_link_model: SocialLinkModel) -> None:
        await self.social_collection.insert_one(social_link_model.model_dump())
    
    async def find_one_by_id(self, id: ObjectId) -> SocialLinkModel | None:
        social_link = await self.social_collection.find_one({"_id": id})
        if social_link:
            return SocialLinkModel(**social_link)
        return social_link
    
    async def update_one_by_id(self, id: ObjectId, social_links_data: SocialLinksUpdateSchema) -> UpdateResult:
        result = await self.social_collection.update_one(
            {"_id": id},
            {"$set":{"instagram": social_links_data.instagram,
                    "facebook": social_links_data.facebook,
                    "x": social_links_data.x,
                    "tiktok": social_links_data.tiktok,
                    "reddit": social_links_data.reddit,
                    "youtube": social_links_data.youtube,
                    "spotify": social_links_data.spotify,
                    "soundcloud": social_links_data.soundcloud,
                    "bandcamp": social_links_data.bandcamp}})
        return result
        