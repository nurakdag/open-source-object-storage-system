import uuid
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Any

from . import crud, schemas, deps
from .database import get_db
from .services import minio_client, publish_event
from .config import settings

router = APIRouter()

@router.post("/buckets", status_code=status.HTTP_201_CREATED, response_model=schemas.Bucket)
def create_bucket(
    bucket_in: schemas.BucketCreate,
    current_user: schemas.TokenData = Depends(deps.admin_role_required)
):
    """
    Create a new bucket. Only accessible by admins.
    """
    bucket_name = bucket_in.name.lower()
    found = minio_client.bucket_exists(bucket_name)
    if found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bucket '{bucket_name}' already exists.",
        )
    minio_client.make_bucket(bucket_name)
    # MinIO'dan bucket oluşturma tarihini almak karmaşık olduğu için şimdilik None dönüyoruz
    # Gerçek bir senaryoda bu bilgi alınabilir veya varsayılan bir değer atanabilir.
    return {"name": bucket_name, "creation_date": "N/A"}


@router.get("/buckets", response_model=List[schemas.Bucket])
def list_buckets(
    current_user: schemas.TokenData = Depends(deps.user_role_required)
):
    """
    List all available buckets.
    """
    buckets = minio_client.list_buckets()
    return [{"name": bucket.name, "creation_date": bucket.creation_date} for bucket in buckets]


@router.get("/objects", response_model=List[schemas.ObjectMetadata])
def list_objects(
    bucket: str = Query(..., description="Bucket name"),
    prefix: str = Query(None, description="Filter objects by prefix"),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(deps.user_role_required)
):
    """
    List objects in a bucket from the database, optionally filtered by a prefix.
    """
    if not minio_client.bucket_exists(bucket):
        raise HTTPException(status_code=404, detail="Bucket not found")
    
    objects = crud.get_objects_by_bucket_and_prefix(db, bucket=bucket, prefix=prefix)
    return objects


@router.post("/objects/presign-upload", response_model=schemas.PresignUploadResponse)
def presign_upload(
    request: schemas.PresignUploadRequest,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(deps.user_role_required)
):
    """
    Get a pre-signed URL for uploading a file.
    """
    if not minio_client.bucket_exists(request.bucket_name):
        raise HTTPException(status_code=404, detail="Bucket not found")

    # Mantıksal versiyonlama için UUID kullan
    version_id = str(uuid.uuid4())
    
    # Pre-signed URL oluştur
    try:
        url = minio_client.presigned_put_object(
            request.bucket_name,
            request.object_key,
            expires=timedelta(seconds=settings.PRESIGN_TTL_SECONDS),
        )
        # Olayı yayınla (dosya henüz yüklenmedi, sadece URL oluşturuldu)
        # Gerçek yükleme sonrası onayı webhook veya başka bir mekanizma ile almak daha doğru olur.
        # MVP için şimdilik burada yayınlıyoruz.
        publish_event("upload_presigned_url_created", {"bucket": request.bucket_name, "key": request.object_key, "user": current_user.email})
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate pre-signed URL: {e}")


@router.post("/objects/presign-download", response_model=schemas.PresignDownloadResponse)
def presign_download(
    request: schemas.PresignDownloadRequest,
    current_user: schemas.TokenData = Depends(deps.user_role_required)
):
    """
    Get a pre-signed URL for downloading a file.
    """
    try:
        url = minio_client.presigned_get_object(
            request.bucket_name,
            request.object_key,
            expires=timedelta(seconds=settings.PRESIGN_TTL_SECONDS),
        )
        publish_event("download_presigned_url_created", {"bucket": request.bucket_name, "key": request.object_key, "user": current_user.email})
        return {"url": url}
    except Exception as e:
        # MinIO client'ı nesne bulunamadığında spesifik bir hata fırlatır, bunu yakalamak daha iyi olur.
        raise HTTPException(status_code=404, detail=f"Object not found or could not generate URL: {e}")
