from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import router as api_router
from .consumer import run_consumer_in_thread

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Audit Service",
    description="Kamu AK-NDS için Denetim Servisi",
    version="0.1.0",
    root_path="/api/audit"
)

# CORS Middleware'ini ekle
origins = [
    "http://localhost",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "http://localhost:3000",
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
    # RabbitMQ consumer'ını arka planda başlat
    run_consumer_in_thread()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"service": "Audit Service", "status": "ok"}
