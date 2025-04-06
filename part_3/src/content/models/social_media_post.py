import uuid
import enum
from src.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import types, Enum, func, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class PlatformType(enum.Enum):
    LINKEDIN = "LINKEDIN"
    FACEBOOK = "FACEBOOK"
    TWITTER = "TWITTER"
    INSTAGRAM = "INSTAGRAM"
    OTHER = "OTHER"


class SocialMediaPosts(Base):
    __tablename__ = 'social_media_posts'
    
    id = Column(types.INTEGER, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), 
                  primary_key=False,
                  unique=True,
                  nullable=False,
                  server_default=func.uuid_generate_v4(),
                  default=uuid.uuid4)
    content = Column(types.TEXT)
    platform_type = Column(Enum(PlatformType))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    workflow_guid = Column(ForeignKey("workflows.guid"))

    image_guid = Column(ForeignKey("images.guid"))
    image = relationship("Images")