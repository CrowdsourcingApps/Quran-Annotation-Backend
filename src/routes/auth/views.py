import smtplib
import ssl
from email.mime.text import MIMEText

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.routes.auth import handler
from src.routes.auth.helper import auth_helper
from src.routes.auth.schema import (EmailMessageSchema, MessageSchema, Token,
                                    UserInSchema, UserOutSchema)
from src.settings import settings
from src.settings.logging import logger

router = APIRouter()


@router.post(
    '/register',
    response_model=Token,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               500: {'description': 'INTERNAL SERVER ERROR'}},
)
async def sign_up(form_data: UserInSchema):
    db_user = await handler.get_user_by_email(email=form_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered')
    user = await handler.create_user(user=form_data)
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
        form_data: OAuth2PasswordRequestForm = Depends()):
    authorized_user = await handler.authenticate_user(form_data.username,
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


@router.get(
    '/me',
    response_model=UserOutSchema,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'}},
)
async def read_users_me(user=Depends(handler.get_current_user)):
    return await UserOutSchema.from_tortoise_orm(user)


@router.post(
    '/token/refresh',
    response_model=Token,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'}},
)
async def refresh(refresh_token: str = Depends(auth_helper.oauth2_scheme)):
    try:
        useremail: str = auth_helper.decode_token(refresh_token)
        user = await handler.get_user_by_email(useremail)
        if user:
            # Create and return token
            access_token = auth_helper.create_access_token(useremail)
            refresh_token = auth_helper.create_refresh_token(useremail)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer',
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    except Exception as ex:
        logger.exception(f'[token] - Decoding error: {ex}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


@router.post(
    '/sendmail',
    response_model=MessageSchema,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               500: {'description': 'INTERNAL SERVER ERROR'}},
)
async def contact_us(form_data: EmailMessageSchema):
    smtp_server = 'smtp.titan.email'
    smtp_port = 465
    username = settings.Website_Email
    password = settings.Email_Password
    sender = form_data.email
    recipients = [settings.Website_Email]
    subject = form_data.name if form_data.name is not None else sender

    # Send the email
    try:
        context = ssl.create_default_context()
        s = smtplib.SMTP_SSL(smtp_server, smtp_port, context)
        s.set_debuglevel(1)
        s.ehlo()
        s.login(username, password)
        msg = MIMEText(form_data.message)
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = f'Message from {subject}'
        s.sendmail(username, recipients, msg.as_string())
        s.close()
        return MessageSchema(info='sucess')
    except Exception as ex:
        logger.exception(f'[Email] - Send Email error: {ex}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
