from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from . import crud, schemas, models, deps, security
from .database import get_db
from .config import settings

router = APIRouter()

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    # Sadece admin yeni kullanıcı kaydedebilir
    current_user: models.User = Depends(deps.admin_role_required),
) -> Any:
    """
    Create new user. Only accessible by admins.
    """
    user = crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.create_user(db=db, user=user_in)
    return user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    user_roles = [role.name.value for role in user.roles]
    access_token = security.create_access_token(
        data={"sub": user.email, "roles": user_roles}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(
    # Burada Redis'e token'ı ekleyerek blacklist'e alacağız.
    # Bu özellik daha sonra eklenecektir.
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Logout user (invalidate token).
    """
    # Token invalidation logic (e.g., using a Redis blacklist) would go here.
    # For MVP, we can return a success message.
    return {"msg": "Successfully logged out"}

@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
