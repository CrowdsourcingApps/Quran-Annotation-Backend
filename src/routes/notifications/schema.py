from pydantic import BaseModel
from src.models import PlatformEnum
from enum import Enum


class AnonymousNotificationToken(BaseModel):
    anonymous_id: int
    token: str
    platform: PlatformEnum


class NotificationToken(BaseModel):
    token: str
    platform: PlatformEnum


class MessageSchema(BaseModel):
    info: str


class TopicEnum(str, Enum):
    AllARUsers = 'all-ar-users'
    AllRUUsers = 'all-ru-users'
    AllENUsers = 'all-en-users'
