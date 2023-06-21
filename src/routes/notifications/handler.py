from src.models import NotificationToken


async def add_notification_token(user_id: int,
                                 token: str,
                                 platform: str) -> NotificationToken:
    notification_token_obj = await NotificationToken.create(user_id=user_id,
                                                            token=token,
                                                            platform=platform)
    return notification_token_obj


async def update_notification_token_user(anonymous_id: int,
                                         user_id):
    result = await NotificationToken.filter(user_id=anonymous_id)\
                                    .update(user_id=user_id)
    if result == 0:
        return False
    return True
