from abc import ABC, abstractmethod
from src.content.schemas.images import ImageCreate, Image

class IImagesRepository(ABC):
    
    @abstractmethod
    async def create_image(self, image_data: ImageCreate) -> Image:
        pass
     