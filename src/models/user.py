from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from src.models import Base

UserRoleEnum = ENUM('annotator', 'admin', 'recitingApp', name='user_role_enum')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_role = Column(UserRoleEnum, default='annotator')
    create_date = Column(DateTime, default=datetime.utcnow)
    validate_correctness_exam_correct_no = Column(Integer, default=0)

    validate_correctness_cts = relationship('ValidateCorrectnessCTUser',
                                            back_populates='user')
