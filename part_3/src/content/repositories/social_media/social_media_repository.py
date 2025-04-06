from sqlalchemy.ext.asyncio import AsyncSession
from src.content.repositories.social_media.social_media_repository_interface import ISocialMediaRepository
from src.content.schemas.social_media_post import SocialMediaCreate, SocialMedia, SocialMediaUpdate
from src.content.models.social_media_post import SocialMediaPosts
from sqlalchemy.future import select

class SocialMediaRepository(ISocialMediaRepository):
    def __init__(self, async_db_session: AsyncSession):
        self.db = async_db_session
        
    async def create_social_media_post(self, social_media_data: SocialMediaCreate) -> SocialMedia:
        if not isinstance(social_media_data, SocialMediaCreate):
            raise ValueError("Expected instance of SocialMediaCreate")
        
        try:
            new_social_media = SocialMediaPosts(content=social_media_data.content, platform_type=social_media_data.platform_type, workflow_guid=social_media_data.workflow_guid)
            self.db.add(new_social_media)
            await self.db.commit()
            await self.db.refresh(new_social_media)
            return SocialMedia(
                id=new_social_media.id,
                guid=new_social_media.guid,
                content=new_social_media.content,
                platform_type=new_social_media.platform_type,
                workflow_guid=new_social_media.workflow_guid
            )
        except:
            await self.db.rollback()
            raise
    async def update_social_media_post(self, blog_id: int, social_media_data: SocialMediaUpdate) -> SocialMedia:
        query = select(SocialMediaPosts).where(SocialMediaPosts.id == blog_id)
        result = await self.db.execute(query)
        sm_post = result.scalars().first()

        if sm_post is None:
            raise Exception("Social Media Post not found")


        for key, value in social_media_data.model_dump().items():
            if value is not None:  
                setattr(sm_post, key, value)

        await self.db.commit()
        await self.db.refresh(sm_post)
        return sm_post