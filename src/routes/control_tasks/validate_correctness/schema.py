from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import ValidateCorrectnessCT

ValidateCorrectnessCTInSchema = pydantic_model_creator(
    ValidateCorrectnessCT,
    name='ValidateCorrectnessCTInSchema',
    exclude=['id', 'golden', 'create_date'])
