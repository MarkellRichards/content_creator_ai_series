from src.content.repositories.images.images_repository_interface import IImagesRepository
from src.content.schemas.images import Image, ImageCreate
from src.content.models.images import Images
from sqlalchemy.ext.asyncio import AsyncSession

class ImageRepository(IImagesRepository):
    def __init__(self, async_db_session: AsyncSession):
        self.db = async_db_session
        
    async def create_image(self, image_data) -> Image:
        if not isinstance(image_data, ImageCreate):
            raise ValueError("Expected instance of ImageCreate")
        
        try: 
            new_image_data = Images(url=image_data.url)
            
            self.db.add(new_image_data)
            await self.db.commit()
            await self.db.refresh(new_image_data)
            
            return Image(
                id=new_image_data.id,
                guid=new_image_data.guid,
                url=new_image_data.url 
                )
        except:
            await self.db.rollback()
            raise
                