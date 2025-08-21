from fastapi import FastAPI
from .database import engine, Base
from .api import router as api_router

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Storage Service",
    description="Kamu AK-NDS için Nesne Depolama Servisi",
    version="0.1.0",
    root_path="/api/storage"
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"service": "Storage Service", "status": "ok"}
