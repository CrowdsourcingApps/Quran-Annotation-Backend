from pydantic import BaseModel
from src.models import PlatformEnum


class AnonymousNotificationToken(BaseModel):
    anonymous_id: int
    token: str
    platform: PlatformEnum


class MessageSchema(BaseModel):
    info: str
