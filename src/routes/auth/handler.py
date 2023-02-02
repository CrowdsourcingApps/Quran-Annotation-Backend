from typing import List

from fastapi import Depends, HTTPException, status
from jose import JWTError

from src.models import User
from src.routes.auth.helper import auth_helper
from src.routes.auth.schema import UserInSchema


async def get_user_by_id(user_id: int) -> User:
    return await User.get_or_none(id=user_id)


async def get_user_by_email(email: str) -> User:
    return await User.get_or_none(email=email)


async def get_current_user(token: str = Depends(auth_helper.oauth2_scheme)
                           ) -> User:
    try:
        user_email = auth_helper.decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    user = await get_user_by_email(user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Could not find user',
        )
    return user


async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    return await User.all().offset(skip).limit(limit).values()


async def create_user(user: UserInSchema):
    hashed_password = auth_helper.get_password_hash(user.password)
    user_obj = await User.create(email=user.email,
                                 hashed_password=hashed_password)
    return user_obj


async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if not user:
        return False
    if not auth_helper.verify_password(password, user.hashed_password):
        return False
    return user


async def update_validate_correctness_exam_correct_no(
        user_id: int, correct_no: int) -> bool:
    result = await User.filter(id=user_id).update(
        validate_correctness_exam_correct_no=correct_no)
    if result == 0:
        return False
    return True
