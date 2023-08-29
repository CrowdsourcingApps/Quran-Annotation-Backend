from typing import List

from pydantic import BaseModel
from src.models import LanguageEnum
from src.routes.notifications.schema import TopicEnum


language_to_topic_mapping = {
    LanguageEnum.AR: TopicEnum.AllARUsers,
    LanguageEnum.EN: TopicEnum.AllENUsers,
    LanguageEnum.RU: TopicEnum.AllRUUsers
}


class CreationError(BaseModel):
    item: str
    message: str


class CreateResponse(BaseModel):
    message: str
    errors: List[CreationError] = []
