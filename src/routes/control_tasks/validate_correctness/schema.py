from typing import List

from pydantic import BaseModel

from src.models import LabelEnum
from src.routes.schema import CreationError


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


class VCCTOutSchema(BaseModel):
    id: int
    surra_number: int
    aya_number: int
    audio_file_name: str
    duration_ms: int
    label: str
    reason_ar: str = None
    reason_en: str = None
    reason_ru: str = None


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
