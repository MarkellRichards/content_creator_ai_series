import uuid
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

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
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class BlogList(BaseModel):
    total: int
    blogs: list[Blog]
    
    
class BlogWithImage(Blog):
    image_url: Optional[str] = None