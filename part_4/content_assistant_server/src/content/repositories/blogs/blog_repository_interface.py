from abc import ABC, abstractmethod
from src.content.schemas.blog_posts import BlogCreate, Blog, BlogUpdate

class IBlogRepository(ABC):
    
    @abstractmethod
    async def create_blog(self, blog_data: BlogCreate) -> Blog:
        pass
    
    @abstractmethod
    async def update_blog(self, blog_data: BlogUpdate) -> Blog:
        pass
    
    @abstractmethod
    async def get_blogs(self, offset: int, limit: int) -> list[Blog]:
        pass
    
    @abstractmethod
    async def get_blog_details(self, blog_id) -> Blog:
        pass