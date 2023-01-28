from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from src.models import Base

LabelEnum = ENUM('correct',
                 'in_correct',
                 'not_related_quran',
                 'not_match_aya',
                 'multiple_aya',
                 name='label_enum')


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
