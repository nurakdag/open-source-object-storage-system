from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import datetime

# Bucket Schemas
class Bucket(BaseModel):
    name: str
    creation_date: datetime

class BucketCreate(BaseModel):
    name: constr(min_length=3, max_length=63)

# Object Schemas
class ObjectMetadata(BaseModel):
    bucket_name: str
    object_key: str
    size: int
    content_type: Optional[str] = None
    version_id: str
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class PresignUploadRequest(BaseModel):
    bucket_name: str
    object_key: str

class PresignUploadResponse(BaseModel):
    url: str
    fields: Optional[dict] = None # Bazı S3 uyumlu sistemler için

class PresignDownloadRequest(BaseModel):
    bucket_name: str
    object_key: str

class PresignDownloadResponse(BaseModel):
    url: str

# Token data for dependency injection
class TokenData(BaseModel):
    email: str | None = None
    roles: List[str] = []
