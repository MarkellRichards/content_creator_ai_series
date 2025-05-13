from sqlalchemy.ext.asyncio import AsyncSession
from src.content.schemas.blog_posts import Blog, BlogCreate, BlogUpdate, BlogList
from src.content.models.blog_posts import BlogPosts
from src.content.repositories.blogs.blog_repository_interface import IBlogRepository
from sqlalchemy.future import select
from src.core.logs import logger
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status

class BlogRepository(IBlogRepository):
    def __init__(self, async_db_session: AsyncSession):
        self.db = async_db_session
        
    async def create_blog(self, blog_data: BlogCreate) -> Blog:
        if not isinstance(blog_data, BlogCreate):
            raise ValueError("Expected a BlogCreate instance")
        
        try:
            new_blog = BlogPosts(title=blog_data.title, content=blog_data.content, workflow_guid=blog_data.workflow_guid)
            self.db.add(new_blog)
            await self.db.commit()
            await self.db.refresh(new_blog)
            return Blog(
                id=new_blog.id,
                guid=new_blog.guid,
                title=new_blog.title,
                content=new_blog.content,
                workflow_guid=new_blog.workflow_guid,
                created_at=new_blog.created_at,
                updated_at=new_blog.updated_at
            )
        except:
            await self.db.rollback()
            raise
        
    async def update_blog(self, blog_id: int, blog_data: BlogUpdate) -> Blog:
        try:
            query = select(BlogPosts).where(BlogPosts.id == blog_id)
            result = await self.db.execute(query)
            blog_post = result.scalars().first()

            if blog_post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Post not found")


            for key, value in blog_data.model_dump().items():
                if value is not None:  
                    setattr(blog_post, key, value)

            await self.db.commit()
            await self.db.refresh(blog_post)
            return blog_post
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
            
        
    
    async def get_blogs(self, offset: int, limit: int) -> BlogList:
        try:
            total_result =  await self.db.execute(select(func.count()).select_from(BlogPosts))
            total = total_result.scalar_one()
            query = select(BlogPosts).options(
            joinedload(BlogPosts.image)
        ).offset(offset).limit(limit)

            result = await self.db.execute(query)
            blogs = result.scalars().all()
            
            blogs_data = [
            {
                "id": blog.id,
                "guid": blog.guid,
                "title": blog.title,
                "content": blog.content[0:400], #slice this to reduce network traffic, details can return full object
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
                "image_url": blog.image.url if blog.image else None, 
            }
            for blog in blogs
        ]
            return {
                "total": total,
                "blogs": blogs_data
            }
        except Exception as e:
            logger.error(f"{e}")
            
    async def get_blog_details(self, blog_guid: str) -> Blog:
        try: 
            
            query = (
                select(BlogPosts).options(
                    joinedload(BlogPosts.image)
                ).where(BlogPosts.guid == blog_guid)
            )
            result = await self.db.execute(query)
            blog_post = result.scalars().first()
            
            if blog_post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
            
            blog_post_data = {
                "id": blog_post.id,
                "guid": blog_post.guid,
                "title": blog_post.title,
                "content": blog_post.content,
                "workflow_guid": blog_post.workflow_guid,
                "created_at": blog_post.created_at,
                "updated_at": blog_post.updated_at,
                "image_url": blog_post.image.url if blog_post.image else None, 
            } 
            return blog_post_data
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        