from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas, deps
from .database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.AuditLog])
def read_audit_logs(
    skip: int = 0,
    limit: int = Query(default=50, lte=200),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(deps.admin_role_required)
):
    """
    Retrieve audit logs. Only accessible by admins.
    """
    logs = crud.get_audit_logs(db, skip=skip, limit=limit)
    return logs
