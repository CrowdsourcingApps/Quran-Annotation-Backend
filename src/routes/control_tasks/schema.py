from typing import List

from pydantic import BaseModel


class CreationError(BaseModel):
    audio: str
    message: str


class CreateResponse(BaseModel):
    message: str
    errors: List[CreationError] = []
