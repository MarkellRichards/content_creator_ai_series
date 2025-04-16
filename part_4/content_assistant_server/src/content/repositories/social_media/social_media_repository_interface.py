from abc import ABC, abstractmethod
from src.content.schemas.social_media_post import SocialMediaCreate, SocialMedia, SocialMediaUpdate

class ISocialMediaRepository(ABC):
    
    @abstractmethod
    async def create_social_media_post(self, social_media_data: SocialMediaCreate) -> SocialMedia:
        pass
    
    @abstractmethod
    async def update_social_media_post(self, social_media_data: SocialMediaUpdate) -> SocialMedia:
        pass
    
    @abstractmethod
    async def get_social_media_post(self, social_media_guid: str) -> SocialMedia:
        pass
    
    @abstractmethod
    async def get_all_social_media_posts(self, offset: int, limit: int) -> list[SocialMedia]:
        pass
    