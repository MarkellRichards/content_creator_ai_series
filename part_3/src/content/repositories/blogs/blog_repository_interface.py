from abc import ABC, abstractmethod
from src.content.schemas.blog_posts import BlogCreate, Blog, BlogUpdate

class IBlogRepository(ABC):
    
    @abstractmethod
    async def create_blog(self, blog_data: BlogCreate) -> Blog:
        pass
    
    @abstractmethod
    async def update_blog(self, blog_data: BlogUpdate) -> Blog:
        pass