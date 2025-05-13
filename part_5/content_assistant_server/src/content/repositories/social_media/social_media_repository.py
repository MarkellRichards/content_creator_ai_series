from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.content.repositories.social_media.social_media_repository_interface import ISocialMediaRepository
from src.content.schemas.social_media_post import SocialMediaCreate, SocialMedia, SocialMediaUpdate, SocialMediaList, SocialMediaWithImage
from src.content.models.social_media_post import SocialMediaPosts
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from src.core.logs import logger

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
                workflow_guid=new_social_media.workflow_guid,
                created_at=new_social_media.created_at,
                updated_at=new_social_media.updated_at
            )
        except:
            await self.db.rollback()
            raise
    async def update_social_media_post(self, blog_id: int, social_media_data: SocialMediaUpdate) -> SocialMedia:
        try: 
            query = select(SocialMediaPosts).where(SocialMediaPosts.id == blog_id)
            result = await self.db.execute(query)
            sm_post = result.scalars().first()

            if sm_post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social Media Post not found")


            for key, value in social_media_data.model_dump().items():
                if value is not None:  
                    setattr(sm_post, key, value)

            await self.db.commit()
            await self.db.refresh(sm_post)
            return sm_post
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
            
    
    async def get_social_media_post(self, social_media_guid):
        try:
            query = (
                select(SocialMediaPosts).options(
                    joinedload(SocialMediaPosts.image)
                ).where(SocialMediaPosts.guid == social_media_guid)
            )
            result = await self.db.execute(query)
            sm_post = result.scalars().first()
        
            if sm_post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social Media Post not found")
        
            sm_posts_data = create_sm_data_dict(sm_post)
            return sm_posts_data
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    async def get_all_social_media_posts(self, offset: int, limit: int) -> SocialMediaList:
        try:
            total_result =  await self.db.execute(select(func.count()).select_from(SocialMediaPosts))
            total = total_result.scalar_one()
            query = (
                select(SocialMediaPosts).options(
                    joinedload(SocialMediaPosts.image)
                ).offset(offset).limit(limit)
            )
            results = await self.db.execute(query)
            sm_posts = results.scalars().all()
            
            sm_data = [create_sm_data_dict(post) for post in sm_posts] 
            return {
                "total": total,
                "social_media_posts": [SocialMediaWithImage.model_validate(sm) for sm in sm_data]
            }
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
        
def create_sm_data_dict(sm_data):
    return {
            "id": sm_data.id,
            "guid": sm_data.guid,
            "content": sm_data.content,
            "platform_type": sm_data.platform_type,
            "workflow_guid": sm_data.workflow_guid,
            "created_at": sm_data.created_at,
            "updated_at": sm_data.updated_at,
            "image_url": sm_data.image.url if sm_data.image else None
        }