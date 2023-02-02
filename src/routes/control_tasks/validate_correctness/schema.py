from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import LabelEnum, ValidateCorrectnessCT

ValidateCorrectnessCTInSchema = pydantic_model_creator(
    ValidateCorrectnessCT,
    name='ValidateCorrectnessCTInSchema',
    exclude=['id', 'golden', 'create_date'])

ValidateCorrectnessCTOutSchema = pydantic_model_creator(
    ValidateCorrectnessCT,
    name='ValidateCorrectnessCTOutSchema',
    exclude=['golden', 'create_date'])


class ValidateCorrectnessExamAnswers(BaseModel):
    ct_id: int
    label: LabelEnum
