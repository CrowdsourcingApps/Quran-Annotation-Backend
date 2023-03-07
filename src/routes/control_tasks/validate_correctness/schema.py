from typing import List

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import LabelEnum, ValidateCorrectnessCT
from src.routes.schema import CreationError

ValidateCorrectnessCTInSchema = pydantic_model_creator(
    ValidateCorrectnessCT,
    name='ValidateCorrectnessCTInSchema',
    exclude=['id', 'golden', 'create_date'])

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
