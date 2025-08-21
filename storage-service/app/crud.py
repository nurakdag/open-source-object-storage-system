from sqlalchemy.orm import Session
from . import models, schemas

def create_object_metadata(db: Session, *, obj_in: schemas.ObjectMetadata, user_email: str, version_id: str):
    db_obj = models.ObjectMetadata(
        bucket_name=obj_in.bucket_name,
        object_key=obj_in.object_key,
        size=obj_in.size,
        content_type=obj_in.content_type,
        version_id=version_id,
        created_by=user_email
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_objects_by_bucket_and_prefix(db: Session, bucket: str, prefix: str, limit: int = 100):
    query = db.query(models.ObjectMetadata).filter(models.ObjectMetadata.bucket_name == bucket)
    if prefix:
        query = query.filter(models.ObjectMetadata.object_key.startswith(prefix))
    return query.limit(limit).all()
