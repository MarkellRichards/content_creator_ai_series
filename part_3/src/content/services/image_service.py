import uuid
import requests
from io import BytesIO
from src.content.repositories.images.images_repository import ImageRepository
from src.content.schemas.images import ImageCreate, Image as ImageSchema
from src.content.models.images import Images
from PIL import Image as PilImage
from botocore.exceptions import NoCredentialsError, ParamValidationError
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from src.core.logs import logger

class ImageService(ImageRepository):
    
    def __init__(self, image_repository: ImageRepository, s3_client):
        self.repository = image_repository
        self.s3_client = s3_client
        
    async def create_image(self, image_data: ImageCreate) -> ImageSchema:
        image = await self.repository.create_image(image_data)
        return ImageSchema.model_validate(image)
    
    @retry(wait=wait_random_exponential(min=1, max=15), stop=stop_after_attempt(3))
    async def generate_image(self, client: OpenAI, prompt: str):
        try:    
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            return response
        except:
            raise Exception("Failed to generate image")
        
    
    async def generate_and_upload_image(self, bucket, openai_client: OpenAI, image_prompt):
        try: 
        
            generated_image = await self.generate_image(client=openai_client, prompt=image_prompt)
            image_url = generated_image.data[0].url
            response = requests.get(image_url)
            image = PilImage.open(BytesIO(response.content))
            image_bytes = BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)

            file_name = f"test_{uuid.uuid4()}.png"
            await self.upload_to_minio(bucket, image_bytes.getvalue(), file_name)
            
            return file_name
        except:
            raise Exception("Failed to upload to minio or create database entry")

    async def upload_to_minio(self, bucket, file_data, filename):
        try:
            self.s3_client.put_object(Bucket=bucket, Key=filename, Body=file_data)
            logger.error(msg=f"Uploaded {filename} to MinIO bucket successfully!")
        except NoCredentialsError:
            logger.error(msg="Credentials not available.")
        except ParamValidationError as e:
            logger.error(msg=f"Parameter validation failed: {e}")