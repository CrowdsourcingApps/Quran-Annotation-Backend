from pydantic import BaseModel

from src.models import LabelEnum


class ValidateCorrectnessTOutSchema(BaseModel):
    id: int
    surra_number: int
    aya_number: int
    audio_file_name: str
    duration_ms: int
    control_task: bool


class ValidateCorrectnessAnswers(BaseModel):
    id: int
    label: LabelEnum
    control_task: bool


class Contribution(BaseModel):
    count: int
