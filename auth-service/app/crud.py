# Bu dosyada, veritabanı üzerinde kullanıcı ve rol ile ilgili temel işlemler (CRUD) tanımlanır.
# Kullanıcı ve rol sorgulama, oluşturma ve şifreleme işlemleri burada yapılır.

from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    # E-posta adresine göre kullanıcıyı getirir
    return db.query(models.User).filter(models.User.email == email).first()

def get_role_by_name(db: Session, role_name: models.RoleEnum):
    # Rol adına göre rolü getirir
    return db.query(models.Role).filter(models.Role.name == role_name).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Yeni kullanıcı oluşturur ve rollerini ekler
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    
    for role_name in user.roles:
        role = get_role_by_name(db, role_name)
        if not role:
            # Roller başlangıçta oluşturulmalı
            raise ValueError(f"Role '{role_name.value}' not found.")
        db_user.roles.append(role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_role(db: Session, role: schemas.RoleCreate):
    # Yeni rol oluşturur
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role