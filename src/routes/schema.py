from typing import List

from pydantic import BaseModel


class CreationError(BaseModel):
    item: str
    message: str


class CreateResponse(BaseModel):
    message: str
    errors: List[CreationError] = []
