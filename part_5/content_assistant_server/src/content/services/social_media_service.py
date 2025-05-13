from src.content.repositories.social_media.social_media_repository import SocialMediaRepository
from src.content.schemas.social_media_post import SocialMedia, SocialMediaCreate, SocialMediaUpdate, SocialMediaWithImage

class SocialMediaService:
    def __init__(self, repository: SocialMediaRepository):
        self.repository = repository
        
    async def create_social_media_post(self, social_media_data: SocialMediaCreate) -> SocialMedia:
        social_media_post = await self.repository.create_social_media_post(social_media_data)
        return SocialMedia.model_validate(social_media_post)
    
    
    async def update_social_media_post(self, sm_id: int, sm_data: SocialMediaUpdate) -> SocialMedia:
        sm = await self.repository.update_social_media_post(sm_id, sm_data)
        return SocialMedia.model_validate(sm)
    
    async def get_all_social_media_posts(self, offset: int, limit: int) -> list[SocialMedia]:
        return await self.repository.get_all_social_media_posts(offset=offset, limit=limit)
         
    
    async def get_social_media_post(self, social_media_guid: str) -> SocialMediaWithImage:
        sm = await self.repository.get_social_media_post(social_media_guid)
        return SocialMediaWithImage.model_validate(sm)