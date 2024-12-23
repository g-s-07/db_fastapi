# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.auth.auth_bearer import JWTBearer
from exceptions.user import user_not_found_exception, incorrect_password_exception, user_already_exists_exception
from helpers.utility import create_access_token, verify_password, get_password_hash
from datetime import timedelta
import os
from app.database import get_db

router = APIRouter()
def get_session_local():
    yield SessionLocal()
    
# @router.get("/users",dependencies=[Depends(JWTBearer())], tags=["users"])
# def get_users(db: Session = Depends(get_db)):
#     return db.query(models.User).all()

# @router.get("/users/{user_id}",dependencies=[Depends(JWTBearer())], tags=["users"])
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     return db.query(models.User).filter(models.User.id == user_id).first()

# @router.post("/users/create", tags=["users"])
# def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(models.User).filter(models.User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered",
#         )
#     hashed_password = get_password_hash(user.password)
#     print(user.password,"not hased")
#     print(hashed_password,"hased")
#     new_user = models.User(fullname=user.fullname, email=user.email, password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))

#     access_token = create_access_token(
#         data={
#             "user_id" : user.email
#         },
#         expires_delta=access_token_expires
#     )
#     return models.Token(access_token=f"Bearer {access_token}")


@router.post("/users/login", tags=["users"])
def login(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise user_not_found_exception
    # if not user.password == password:
    if not verify_password(password, user.password):
        raise incorrect_password_exception
    access_token_expires = timedelta(days=int(os.environ.get("ACCESS_TOKEN_EXPIRE_DAYS")))

    access_token = create_access_token(
        data={
            "user_id" : user.email
        },
        expires_delta=access_token_expires
    )
    return models.Token(access_token=f"Bearer {access_token}")