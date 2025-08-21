from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/api/auth/login")

def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> schemas.TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, roles=roles)
    except JWTError:
        raise credentials_exception
    return token_data

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: schemas.TokenData = Depends(get_current_user_from_token)):
        if not any(role in self.allowed_roles for role in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this role",
            )
        return user

admin_role_required = RoleChecker(["ADMIN"])
