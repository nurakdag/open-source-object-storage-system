# Bu dosyada, API için veri doğrulama ve veri transferi amacıyla Pydantic şemaları tanımlanır.
# Kullanıcı, rol ve token ile ilgili istek/yanıt yapıları burada belirlenir.
# RoleEnum ile rol tipleri, User şemaları ile kullanıcı bilgileri ve Token şemaları 
# ile kimlik doğrulama yapısı oluşturulur.

from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from .models import RoleEnum

# Rol ile ilgili temel şema
class RoleBase(BaseModel):
    name: RoleEnum  # Rol adı (enum)

# Rol oluşturma isteği için şema
class RoleCreate(RoleBase):
    pass  # Ek alan yok, RoleBase ile aynı

# Rol yanıtı için şema
class Role(RoleBase):
    id: int  # Rol ID'si

    class Config:
        from_attributes = True  # ORM'den veri aktarımı için

# Kullanıcı ile ilgili temel şema
class UserBase(BaseModel):
    email: EmailStr  # Kullanıcı e-posta adresi

# Kullanıcı oluşturma isteği için şema
class UserCreate(UserBase):
    password: str  # Kullanıcı şifresi
    roles: List[RoleEnum] = [RoleEnum.USER]  # Varsayılan rol

# Kullanıcı yanıtı için şema
class User(UserBase):
    id: int  # Kullanıcı ID'si
    is_active: bool  # Kullanıcı aktif mi?
    roles: List[Role] = []  # Kullanıcının rolleri
    created_at: datetime  # Oluşturulma zamanı

    class Config:
        from_attributes = True  # ORM'den veri aktarımı için

# Token yanıtı için şema
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# Token içeriği için şema
class TokenData(BaseModel):
    email: EmailStr | None = None  # Kullanıcı e-posta adresi (isteğe bağlı)
    roles: List[str] = []          #
