from datetime import datetime
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


async def update_notification_token_date(token: str):
    date = datetime.utcnow()
    result = await NotificationToken.filter(token=token)\
                                    .update(update_date=date)
    if result == 0:
        return False
    return True


async def token_exist(token: str) -> bool:
    result = await NotificationToken.get_or_none(token=token)

    if result is None:
        return False
    return True
