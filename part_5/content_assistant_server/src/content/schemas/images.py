import uuid
from pydantic import BaseModel

class ImageCreate(BaseModel):
    url: str
    
class Image(BaseModel):
    id: int
    guid: uuid.UUID
    url: str
    
    class Config:
        from_attributes = True