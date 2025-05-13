from src.content.repositories.blogs.blog_repository import BlogRepository
from src.content.schemas.blog_posts import Blog, BlogCreate, BlogUpdate, BlogWithImage

class BlogService:
    def __init__(self, repository: BlogRepository):
        self.repository = repository
        
    async def create_blog(self, blog_data: BlogCreate) -> Blog:
        blog = await self.repository.create_blog(blog_data)
        return Blog.model_validate(blog)
    
    async def update_blog(self, blog_id: int, blog_data: BlogUpdate) -> Blog:
        blog = await self.repository.update_blog(blog_id, blog_data)
        return Blog.model_validate(blog)
    
    async def get_blogs(self, offset: int, limit: int) -> list[Blog]:
        return await self.repository.get_blogs(offset, limit)
    
    async def get_blog_details(self, blog_guid: str) -> BlogWithImage:
        blog = await self.repository.get_blog_details(blog_guid)
        return BlogWithImage.model_validate(blog)
        