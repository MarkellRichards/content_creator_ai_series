import uuid
import enum
from sqlalchemy import Column, Enum, types, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.core.database import Base


class WorkflowStatusType(enum.Enum):
    INPROGRESS = "INPROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(types.INTEGER, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), 
                  primary_key=False, 
                  unique=True,
                  nullable=False,
                  server_default=func.uuid_generate_v4(),
                  default=uuid.uuid4)
    status = Column(Enum(WorkflowStatusType), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    blog_posts = relationship("BlogPosts", back_populates="workflow", lazy="select")
    social_media_posts = relationship("SocialMediaPosts", back_populates="workflow", lazy="select")