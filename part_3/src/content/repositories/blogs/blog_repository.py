from sqlalchemy.ext.asyncio import AsyncSession
from src.content.schemas.blog_posts import Blog, BlogCreate, BlogUpdate
from src.content.models.blog_posts import BlogPosts
from src.content.repositories.blogs.blog_repository_interface import IBlogRepository
from sqlalchemy.future import select

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
                workflow_guid=new_blog.workflow_guid
            )
        except:
            await self.db.rollback()
            raise
        
    async def update_blog(self, blog_id: int, blog_data: BlogUpdate) -> Blog:
        query = select(BlogPosts).where(BlogPosts.id == blog_id)
        result = await self.db.execute(query)
        blog_post = result.scalars().first()

        if blog_post is None:
            raise Exception("Blog Post not found")


        for key, value in blog_data.model_dump().items():
            if value is not None:  
                setattr(blog_post, key, value)

        await self.db.commit()
        await self.db.refresh(blog_post)
        return blog_post