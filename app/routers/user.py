from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.auth.auth import create_access_token, authenticate_user, get_current_active_user
from app.crud.user import create_user, get_user_by_username, update_user
from dependencies import get_db
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username is already taken",
        )
    new_user = create_user(db=db, user=user)
    return new_user


@router.post("/login")
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_user_profile(
        current_user: User = Depends(get_current_active_user)
):
    return current_user


@router.put("/me", response_model=UserOut)
def update_user_profile(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):
    updated_user = update_user(db=db, user_id=current_user.id, user_update=user_update)
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return updated_user
