from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .api import router as api_router
from .database import engine, SessionLocal, get_db
from .config import settings

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Kamu AK-NDS için Kimlik Doğrulama Servisi",
    version="0.1.0",
    root_path="/api/auth"
)

# CORS Middleware'ini ekle
# Bu, farklı origin'lerden (örneğin localhost:8002'deki storage-service docs)
# gelen isteklere izin verir.
origins = [
    "http://localhost",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "http://localhost:3000", # React app için
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """
    Uygulama başlangıcında varsayılan rolleri ve admin kullanıcısını oluştur.
    """
    db = SessionLocal()
    try:
        # Rolleri oluştur
        admin_role = crud.get_role_by_name(db, models.RoleEnum.ADMIN)
        if not admin_role:
            crud.create_role(db, schemas.RoleCreate(name=models.RoleEnum.ADMIN))
        
        user_role = crud.get_role_by_name(db, models.RoleEnum.USER)
        if not user_role:
            crud.create_role(db, schemas.RoleCreate(name=models.RoleEnum.USER))

        # Varsayılan admin kullanıcısını oluştur
        admin_user = crud.get_user_by_email(db, email=settings.DEFAULT_ADMIN_EMAIL)
        if not admin_user:
            admin_user_in = schemas.UserCreate(
                email=settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,
                roles=[models.RoleEnum.ADMIN, models.RoleEnum.USER]
            )
            crud.create_user(db, admin_user_in)
    finally:
        db.close()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"service": "Auth Service", "status": "ok"}
