from typing import List

from fastapi import Depends, HTTPException, status
from jose import JWTError

from src.models import User
from src.routes.auth.helper import auth_helper
from src.routes.auth.schema import UserInSchema
from src.routes.notifications.handler import update_notification_token_user


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


async def create_anonumous():
    user_obj = await User.create(is_anonymous=True)
    return user_obj


async def get_anonumous(anonymous_id):
    user_obj = await User.get_or_none(is_anonymous=True, id=anonymous_id)
    return user_obj


async def remove_anonumous(anonymous_id: int) -> bool:
    result = await User.filter(is_anonymous=True, id=anonymous_id).delete()
    if result == 0:
        return False
    return True


async def transfare_anonymous(anonymous_id: int, user: UserInSchema) -> bool:
    hashed_password = auth_helper.get_password_hash(user.password)
    result = await User.filter(id=anonymous_id).update(
                                            email=user.email,
                                            hashed_password=hashed_password,
                                            is_anonymous=False)
    if result == 0:
        return False
    return True


async def remove_anonymous_account(anonymous_id: int, user_id: int) -> bool:
    # move tokens
    # TODO Refactoring: Move update_notification_token_user
    await update_notification_token_user(anonymous_id, user_id)

    # delete anonymous account
    result = await remove_anonumous(anonymous_id)

    return result


async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if not user:
        return False
    if not auth_helper.verify_password(password, user.hashed_password):
        return False
    return user


async def update_validate_correctness_exam_status(
        user_id: int) -> bool:
    result = await User.filter(id=user_id).update(
        validate_correctness_exam_pass=True)
    if result == 0:
        return False
    return True


async def update_user_validate_correctness_tasks_no(
        user: User, num: int) -> bool:
    old = user.validate_correctness_tasks_no
    new = old + num
    result = await User.filter(id=user.id).update(
        validate_correctness_tasks_no=new)
    if result == 0:
        return False
    return True


async def update_user_language(
        user_id: int, lang: str) -> bool:
    result = await User.filter(id=user_id).update(
        language=lang)
    if result == 0:
        return False
    return True
