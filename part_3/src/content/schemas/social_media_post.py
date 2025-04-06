import uuid
from typing import Optional
from enum import Enum
from pydantic import BaseModel

class PlatformType(str, Enum):
    LINKEDIN = "LINKEDIN"
    FACEBOOK = "FACEBOOK"
    TWITTER = "TWITTER"
    INSTAGRAM = "INSTAGRAM"
    OTHER = "OTHER"

class SocialMediaCreate(BaseModel):
    content: str
    platform_type: PlatformType
    workflow_guid: uuid.UUID
    
class SocialMediaUpdate(BaseModel):
    id: int
    content: Optional[str] = None
    platform_type: Optional[PlatformType] = None
    workflow_guid: Optional[uuid.UUID] = None
    image_guid: Optional[uuid.UUID] = None

class SocialMedia(BaseModel):
    id: int
    guid: uuid.UUID
    content: str
    platform_type: PlatformType
    workflow_guid: uuid.UUID

    class Config:
        from_attributes = True