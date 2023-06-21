from fastapi import APIRouter, HTTPException, status
from src.routes.notifications.schema import (AnonymousNotificationToken,
                                             MessageSchema)
from src.routes.auth.handler import get_anonumous
from src.routes.notifications import handler

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

    # TODO check validity of notification token

    notification_token = await handler.add_notification_token(
        user_id=body.anonymous_id,
        token=body.token,
        platform=body.platform)
    if notification_token is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='failed to save the notification token',
        )
    return MessageSchema(info='Success')
