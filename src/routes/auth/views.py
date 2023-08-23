import asyncio
import re
import smtplib
import ssl
from email.mime.text import MIMEText

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.routes.auth import handler
from src.routes.auth.helper import auth_helper
from src.routes.auth.schema import (EmailMessageSchema, MessageSchema, Token,
                                    UserInSchema, UserOutSchema, Anonymous,
                                    langSchema, language_to_topic_mapping,
                                    AnonymouslangSchema)
from src.routes.notifications.helper import notification_helper
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
async def sign_up(form_data: UserInSchema, anonymous_id: int = None):
    email = form_data.email.strip()

    # Email validation pattern
    email_pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

    # Check if the trimmed string matches the email pattern
    if not re.match(email_pattern, email):
        # Valid email format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email Not Valid')
    db_user = await handler.get_user_by_email(email=email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered')
    form_data.email = email

    if anonymous_id is not None:
        # check validity of anonymous_id
        anonymous_user = await handler.get_anonumous(anonymous_id)
        if anonymous_user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid Anonymous User')
        result = await handler.transfare_anonymous(anonymous_id=anonymous_id,
                                                   user=form_data)
        if result is False:
            logger.exception(f'[db] - Remove anonymusity user {anonymous_id}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Remove anonymusity user failed')

    else:
        user = await handler.create_user(user=form_data)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='failed to create new user',
            )

    access_token = auth_helper.create_access_token(form_data.email)
    refresh_token = auth_helper.create_refresh_token(form_data.email)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post(
    '/register_anonumous',
    response_model=Anonymous,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               500: {'description': 'INTERNAL SERVER ERROR'}},
)
async def sign_up_anonumous():
    user = await handler.create_anonumous()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='failed to create new user',
        )
    id = user.id
    return Anonymous(anonymous_id=id)


@router.post(
    '/token',
    response_model=Token,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               401: {'description': 'UNAUTHORIZED'}},
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        anonymous_id: int = None):
    email = form_data.username.strip()
    # Email validation pattern
    email_pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

    # Check if the trimmed string matches the email pattern
    if not re.match(email_pattern, email):
        # Valid email format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email Not Valid')
    authorized_user = await handler.authenticate_user(email,
                                                      form_data.password)
    if not authorized_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if anonymous_id is not None:
        # check validity of anonymous_id
        anonymous_user = await handler.get_anonumous(anonymous_id)
        user_id = authorized_user.id
        if anonymous_user and anonymous_id != user_id:
            # remove anonymous account after transfare notification tokes
            result = await handler.remove_anonymous_account(anonymous_id,
                                                            user_id)
            if result is False:
                logger.exception(f'[db] - removing {anonymous_id} failed')

    access_token = auth_helper.create_access_token(authorized_user.email)
    refresh_token = auth_helper.create_refresh_token(authorized_user.email)
    return Token(access_token=access_token, refresh_token=refresh_token)


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
    

@router.get(
    '/me',
    response_model=UserOutSchema,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'}},
)
async def get_user_info(user=Depends(handler.get_current_user)):
    return await UserOutSchema.from_tortoise_orm(user)


@router.put(
    '/language',
    response_model=MessageSchema,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               401: {'description': 'UNAUTHORIZED'}},
)
async def update_language(language: langSchema,
                          user=Depends(handler.get_current_user)):
    old_language = user.language
    new_language = language.language
    if old_language == new_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You have not changed the language')
    result = await handler.update_user_language(user.id, new_language)
    if result is True:
        # successfully update language
        # Retrieve related notificationtokens
        notification_tokens = await user.notificationtokens.all()

        # Extract token values from related objects
        token_values = [token.token for token in notification_tokens]

        # subscribe to different Topic
        old_topic = language_to_topic_mapping.get(old_language)
        new_topic = language_to_topic_mapping.get(new_language)
        asyncio.create_task(notification_helper.unsubscribe_subscribe_topic(
                                                    old_topic,
                                                    new_topic,
                                                    token_values))
    return MessageSchema(info='success')


@router.put(
    '/language_anonymous',
    response_model=MessageSchema,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               401: {'description': 'UNAUTHORIZED'}},
)
async def update_language_anonymous(anon_language: AnonymouslangSchema):
    anonymous_user = await handler.get_user_by_id(anon_language.anonymous_id)
    old_language = anonymous_user.language
    new_language = anon_language.language
    if old_language == new_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You have not changed the language')
    result = await handler.update_user_language(anon_language.anonymous_id,
                                                new_language)
    if result is True:
        # successfully update language
        # Retrieve related notificationtokens
        notification_tokens = await anonymous_user.notificationtokens.all()

        # Extract token values from related objects
        token_values = [token.token for token in notification_tokens]

        if len(token_values) > 0:
            # subscribe to different Topic
            old_topic = language_to_topic_mapping.get(old_language)
            new_topic = language_to_topic_mapping.get(new_language)
            asyncio.create_task(
                notification_helper.unsubscribe_subscribe_topic(
                                                        old_topic,
                                                        new_topic,
                                                        token_values)
            )
    return MessageSchema(info='success')


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
        return MessageSchema(info='success')
    except Exception as ex:
        logger.exception(f'[Email] - Send Email error: {ex}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
