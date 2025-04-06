from abc import ABC, abstractmethod
from src.content.schemas.social_media_post import SocialMediaCreate, SocialMedia, SocialMediaUpdate

class ISocialMediaRepository(ABC):
    
    @abstractmethod
    async def create_social_media_post(self, social_media_data: SocialMediaCreate) -> SocialMedia:
        pass
    
    @abstractmethod
    async def update_social_media_post(self, social_media_data: SocialMediaUpdate) -> SocialMedia:
        pass
    