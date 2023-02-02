from pydantic import BaseModel


class ValidateCorrectnessTOutSchema(BaseModel):
    id: int
    surra_number: int
    aya_number: int
    audio_file_name: str
    duration_ms: int
    control_task: bool
