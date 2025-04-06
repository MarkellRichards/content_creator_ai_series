import uuid
from typing import Optional
from pydantic import BaseModel

class BlogCreate(BaseModel):
    title: str
    content: str
    workflow_guid: uuid.UUID
    
class BlogUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None
    workflow_guid: Optional[uuid.UUID] = None
    image_guid: Optional[uuid.UUID] = None
    
class Blog(BaseModel):
    id: int
    guid: uuid.UUID
    title: str
    content: str
    workflow_guid: uuid.UUID
    
    class Config:
        from_attributes = True