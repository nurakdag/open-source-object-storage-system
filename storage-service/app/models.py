from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class ObjectMetadata(Base):
    __tablename__ = "object_metadata"

    id = Column(Integer, primary_key=True, index=True)
    bucket_name = Column(String, index=True, nullable=False)
    object_key = Column(String, index=True, nullable=False)
    size = Column(Integer)
    content_type = Column(String)
    version_id = Column(String, unique=True) # Mantıksal versiyonlama için
    created_by = Column(String, nullable=False) # User email
    created_at = Column(DateTime(timezone=True), server_default=func.now())
