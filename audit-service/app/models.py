from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True, nullable=False)
    principal = Column(String, index=True, nullable=False) # Olayı gerçekleştiren kullanıcı (örn: user@demo.gov)
    details = Column(JSON) # Olaya dair ek detaylar (örn: bucket, key)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
