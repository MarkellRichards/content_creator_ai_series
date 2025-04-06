import uuid
from src.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import types, func, Column, DateTime

class Images(Base):
    __tablename__ = 'images'
    
    id = Column(types.INTEGER, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), 
                  primary_key=False,
                  unique=True,
                  nullable=False,
                  server_default=func.uuid_generate_v4(),
                  default=uuid.uuid4)
    url = Column(types.String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)