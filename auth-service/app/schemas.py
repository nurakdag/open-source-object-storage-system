from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from .models import RoleEnum

# Role Schemas
class RoleBase(BaseModel):
    name: RoleEnum

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    roles: List[RoleEnum] = [RoleEnum.USER]

class User(UserBase):
    id: int
    is_active: bool
    roles: List[Role] = []
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None
    roles: List[str] = []
