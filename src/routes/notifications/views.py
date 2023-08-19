import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from src.routes.notifications.schema import (AnonymousNotificationToken,
                                             MessageSchema,
                                             NotificationToken,
                                             TopicEnum)
from src.routes.auth.handler import get_anonumous
from src.routes.notifications import handler
from src.routes.notifications.helper import notification_helper
from src.routes.auth.handler import get_current_user

router = APIRouter()


@router.post(
    '/store_token_anonymous',
    response_model=MessageSchema,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               500: {'description': 'INTERNAL SERVER ERROR'}},
)
async def store_token_anonymous(body: AnonymousNotificationToken):
    # anonymous_id should be registered
    anonymous_user = await get_anonumous(body.anonymous_id)
    if anonymous_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid Anonymous User')

    # check if token is already exist
    token_exist = await handler.token_exist(token=body.token)
    if token_exist:
        # update the date of token
        result = await handler.update_notification_token_date(token=body.token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='failed to update the notification token date',
            )
    else:
        # TODO check validity of notification token

        # store the token in db
        notification_token = await handler.add_notification_token(
            user_id=body.anonymous_id,
            token=body.token,
            platform=body.platform)
        if notification_token is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='failed to save the notification token',
            )

        # TODO bring language from user profile to subscribe the suitable topic

        # subscribe token to the topic AllUsers in the background
        asyncio.create_task(notification_helper.subscribe_topic(
                                            [notification_token.token],
                                            TopicEnum.AllARUsers))
    return MessageSchema(info='Success')


@router.post(
    '/store_token',
    response_model=MessageSchema,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'},
               500: {'description': 'INTERNAL SERVER ERROR'}},
)
async def store_token(body: NotificationToken,
                      user=Depends(get_current_user)):
    # check if token is already exist
    token_exist = await handler.token_exist(token=body.token)
    if token_exist:
        # update the date of token
        result = await handler.update_notification_token_date(token=body.token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='failed to update the notification token date',
            )
    else:
        # TODO check validity of notification token

        notification_token = await handler.add_notification_token(
            user_id=user.id,
            token=body.token,
            platform=body.platform)
        if notification_token is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='failed to save the notification token',
            )

        # TODO bring language from user profile to subscribe the suitable topic

        # subscribe token to the topic AllUsers in the background
        asyncio.create_task(notification_helper.subscribe_topic(
                                        [notification_token.token],
                                        TopicEnum.AllARUsers))
    return MessageSchema(info='Success')
