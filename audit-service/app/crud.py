from sqlalchemy.orm import Session
from . import models, schemas

def create_audit_log(db: Session, log: schemas.AuditLogCreate):
    db_log = models.AuditLog(
        event_type=log.event_type,
        principal=log.principal,
        details=log.details
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_audit_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).offset(skip).limit(limit).all()
