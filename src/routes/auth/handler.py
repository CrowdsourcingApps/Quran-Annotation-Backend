from typing import List

from fastapi import Depends
from jose import JWTError
from sqlalchemy.orm import Session

from src.models import User
from src.routes.auth.helper import auth_helper
from src.routes.auth.schema import UserInSchema


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_current_user(db: Session,
                     token: str = Depends(auth_helper.oauth2_scheme)
                     ) -> User:
    try:
        user_email = auth_helper.decode_token(token)
    except JWTError:
        return None
    user = get_user_by_email(db, user_email)
    if user is None:
        raise None
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserInSchema):
    hashed_password = auth_helper.get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password,)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not auth_helper.verify_password(password, user.hashed_password):
        return False
    return user

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
