from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src import get_db
from src.routes.auth import handler
from src.routes.auth.helper import auth_helper
from src.routes.auth.schema import Token, UserInSchema

router = APIRouter()


@router.post(
    '/register',
    response_model=Token,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               500: {'description': 'INTERNAL SERVER ERROR'}},
)
async def sign_up(
        form_data: UserInSchema, db: Session = Depends(get_db)):
    db_user = handler.get_user_by_email(db, email=form_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered')
    user = handler.create_user(db=db, user=form_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='failed to create new user',
        )
    access_token = auth_helper.create_access_token(user.email)
    refresh_token = auth_helper.create_refresh_token(user.email)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post(
    '/token',
    response_model=Token,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'}},
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    authorized_user = handler.authenticate_user(db,
                                                form_data.username,
                                                form_data.password)
    if not authorized_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = auth_helper.create_access_token(authorized_user.email)
    refresh_token = auth_helper.create_refresh_token(authorized_user.email)
    return Token(access_token=access_token, refresh_token=refresh_token)
