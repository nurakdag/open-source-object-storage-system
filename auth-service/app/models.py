# Bu dosyada, kullanıcı ve rol veritabanı modelleri tanımlanır.
# User ve Role tabloları ile aralarındaki çoklu ilişki (çoktan çoğa) yapılandırılır.
# Ayrıca rol tipleri için sabit değerler (enum) belirlenir.

import enum # Sabit değerleri tanımlayan bir sınıf

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"  # Yönetici rolü
    USER = "USER"    # Normal kullanıcı rolü

# Kullanıcı ve rol arasındaki çoktan çoğa ilişkiyi tanımlayan yardımcı tablo
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Kullanıcı ID'si
    email = Column(String, unique=True, index=True, nullable=False)  # Kullanıcı e-posta adresi
    hashed_password = Column(String, nullable=False)  # Şifre (hashlenmiş)
    is_active = Column(Boolean, default=True)  # Kullanıcı aktif mi?
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Oluşturulma zamanı
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Güncellenme zamanı

    roles = relationship("Role", secondary=user_roles, back_populates="users")  # Kullanıcının rolleri

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)  # Rol ID'si
    name = Column(Enum(RoleEnum), unique=True, nullable=False)  # Rol adı (enum)

    users = relationship("User", secondary=user_roles, back_populates="roles")  # Role