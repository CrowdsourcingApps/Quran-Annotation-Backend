from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class UserRoleEnum(str, Enum):
    Admin = 'admin'
    RecitingApp = 'reciting_app'
    Annotator = 'annotator'


class UserUpdateSchema(BaseModel):
    email: str


VALIDATE_CORRECTNESS_THRESHOLD = 0.7


class UserOutSchema(UserUpdateSchema):
    id: str
    user_role: UserRoleEnum = UserRoleEnum.Annotator
    create_date: datetime = datetime.now()
    validate_correctness_exam_correct_no: int = 0


class UserInSchema(BaseModel):
    email: str
    password: str


class MessageSchema(BaseModel):
    info: str
