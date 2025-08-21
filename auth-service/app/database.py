# Bu dosyada, SQLAlchemy kullanılarak veritabanı bağlantısı ve oturumu (session) yönetimi sağlanıyor.
# engine: Veritabanı bağlantısını oluşturur.
# SessionLocal: Veritabanı işlemleri için oturum (session) nesnesi üretir.
# Base: SQLAlchemy modellerinin temelini oluşturur.
# get_db(): Her istekte kullanılacak veritabanı oturumunu açar ve iş bitince kapatır.
# Kısacası, bu dosya uygulamanın veritabanı ile etkileşim kurmasını sağlar.


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
