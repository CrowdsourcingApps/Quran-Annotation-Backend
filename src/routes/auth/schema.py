from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import User


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class UserUpdateSchema(BaseModel):
    email: str


VALIDATE_CORRECTNESS_THRESHOLD = 0.7


UserOutSchema = pydantic_model_creator(User, name='User',
                                       exclude=['hashed_password',
                                                'validate_correctness_cts'])


class UserInSchema(BaseModel):
    email: str
    password: str


class MessageSchema(BaseModel):
    info: str
