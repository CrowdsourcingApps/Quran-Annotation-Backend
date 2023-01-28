from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.models import Base
from src.models.validate_correctness_ct import LabelEnum


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
