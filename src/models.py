from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from src import Base

UserRoleEnum = ENUM('annotator', 'admin', 'recitingApp', name='user_role_enum')
LabelEnum = ENUM('correct',
                 'in_correct',
                 'not_related_quran',
                 'not_match_aya',
                 'multiple_aya',
                 name='label_enum')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    surra_number = Column(Integer)
    aya_number = Column(Integer)
    audio_file_name = Column(String)
    duration_ms = Column(Integer)
    create_date = Column(DateTime, default=None)
    client_id = Column(String)
    final_transcription = Column(String)
    label = Column(LabelEnum)
    validated = Column(Boolean, default=False)


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


class ValidateCorrectnessCTUser(Base):
    __tablename__ = 'validate_correctness_cts_users'

    id = Column(Integer, primary_key=True)
    validate_correctness_ct_id = Column(
        Integer,
        ForeignKey('validate_correctness_cts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    test = Column(Boolean, default=False)
    label = Column(LabelEnum)
    create_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='validate_correctness_cts')
    validate_correctness_control_task = relationship(
        'ValidateCorrectnessControlTask',
        back_populates='users')


class ValidateCorrectnessControlTask(Base):
    __tablename__ = 'validate_correctness_cts'
    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(String)
    surra_number = Column(Integer)
    aya_number = Column(Integer)
    audio_file_name = Column(String)
    duration_ms = Column(Integer)
    create_date = Column(DateTime, default=datetime.utcnow)
    surra_aya = Column(String)
    golden = Column(Boolean)
    label = Column(LabelEnum)

    users = relationship('ValidateCorrectnessCTUser',
                         back_populates='validate_correctness_control_task')
