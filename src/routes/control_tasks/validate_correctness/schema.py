from typing import List

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import LabelEnum, ValidateCorrectnessCT
from src.routes.schema import CreationError

# ValidateCorrectnessCTInSchema = pydantic_model_creator(
#     ValidateCorrectnessCT,
#     name='ValidateCorrectnessCTInSchema',
#     exclude=['id', 'golden', 'create_date'])


class VCCTInSchema(BaseModel):
    surra_number: int
    aya_number: int
    client_id: str
    audio_file_name: str
    duration_ms: int
    label: str
    reason_ar: str = None
    reason_en: str = None
    reason_ru: str = None


ValidateCorrectnessCTOutSchema = pydantic_model_creator(
    ValidateCorrectnessCT,
    name='ValidateCorrectnessCTOutSchema',
    exclude=['golden', 'create_date', 'client_id'])


class ValidateCorrectnessExamAnswers(BaseModel):
    id: int
    label: LabelEnum


class TestResponse(BaseModel):
    message: str
    pass_exam: bool
    score: float
    errors: List[CreationError] = []


class UserPerformance(BaseModel):
    acc: float


class GoldenReasonVcCt(BaseModel):
    validatecorrectnessct_id: int
    reason_ar: str
    reason_en: str = None
    reason_ru: str = None
