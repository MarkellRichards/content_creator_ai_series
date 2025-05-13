import uuid
from src.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import types, ForeignKey, func, DateTime, Column
from sqlalchemy.orm import relationship

class BlogPosts(Base):
    __tablename__ = 'blog_posts'
    
    id = Column(types.INTEGER, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), 
                  primary_key=False,
                  unique=True,
                  nullable=False,
                  server_default=func.uuid_generate_v4(),
                  default=uuid.uuid4)
    title = Column(types.String)
    content = Column(types.TEXT)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    workflow_guid = Column(ForeignKey("workflows.guid"))
    workflow = relationship("Workflow", back_populates="blog_posts")
    
    image_guid = Column(ForeignKey("images.guid"))
    image = relationship("Images")
    