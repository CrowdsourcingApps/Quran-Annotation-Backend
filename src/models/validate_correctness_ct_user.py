from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models import Base
from src.models.validate_correctness_ct import LabelEnum


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
