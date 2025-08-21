from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# AuditLog Schemas
class AuditLogBase(BaseModel):
    event_type: str
    principal: str
    details: Optional[Dict[str, Any]] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Token data for dependency injection
class TokenData(BaseModel):
    email: str | None = None
    roles: List[str] = []
