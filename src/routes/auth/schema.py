from pydantic import BaseModel, constr
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import User, LanguageEnum
from src.routes.notifications.schema import TopicEnum

language_to_topic_mapping = {
    LanguageEnum.AR: TopicEnum.AllARUsers,
    LanguageEnum.EN: TopicEnum.AllENUsers,
    LanguageEnum.RU: TopicEnum.AllRUUsers
}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class UserUpdateSchema(BaseModel):
    email: str


class Anonymous(BaseModel):
    anonymous_id: int


VALIDATE_CORRECTNESS_THRESHOLD = 0.7


UserOutSchema = pydantic_model_creator(User, name='User',
                                       exclude=['hashed_password',
                                                'validate_correctness_cts'])


class UserInSchema(BaseModel):
    email: str
    password: constr(min_length=8, max_length=128)


class MessageSchema(BaseModel):
    info: str


class EmailMessageSchema(BaseModel):
    email: str
    name: str = None
    message: str


class langSchema(BaseModel):
    language: LanguageEnum
