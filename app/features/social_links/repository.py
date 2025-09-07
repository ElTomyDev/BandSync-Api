from bson import ObjectId
from fastapi import Request
from pymongo.results import UpdateResult

from app.features.social_links.schema import UpdateSocialLinksSchema

class SocialLinksRepository:
    def __init__(self, request: Request) -> None:
        self.__user_collection = request.app.state.db['users']
    
    async def update_one(self, username: str, user_id: str, social_links_data: UpdateSocialLinksSchema) -> UpdateResult:
        if username == None:
            update_result = await self.__user_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set":{"social_links.instagram": social_links_data.instagram,
                        "social_links.facebook": social_links_data.facebook,
                        "social_links.x": social_links_data.x,
                        "social_links.tiktok": social_links_data.tiktok,
                        "social_links.reddit": social_links_data.reddit,
                        "social_links.youtube": social_links_data.youtube,
                        "social_links.spotify": social_links_data.spotify,
                        "social_links.soundcloud": social_links_data.soundcloud,
                        "social_links.bandcamp": social_links_data.bandcamp}})
            return update_result
        update_result = await self.__user_collection.update_one(
                {"username": username},
                {"$set":{"social_links.instagram": social_links_data.instagram,
                        "social_links.facebook": social_links_data.facebook,
                        "social_links.x": social_links_data.x,
                        "social_links.tiktok": social_links_data.tiktok,
                        "social_links.reddit": social_links_data.reddit,
                        "social_links.youtube": social_links_data.youtube,
                        "social_links.spotify": social_links_data.spotify,
                        "social_links.soundcloud": social_links_data.soundcloud,
                        "social_links.bandcamp": social_links_data.bandcamp}})
        return update_result