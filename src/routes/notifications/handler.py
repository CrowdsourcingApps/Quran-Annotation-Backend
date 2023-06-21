from src.models import NotificationToken


async def add_notification_token(user_id: int,
                                 token: str,
                                 platform: str) -> NotificationToken:
    notification_token_obj = await NotificationToken.create(user_id=user_id,
                                                            token=token,
                                                            platform=platform)
    return notification_token_obj
