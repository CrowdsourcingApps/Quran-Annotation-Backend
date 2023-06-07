from pydantic import BaseModel


class Statistics(BaseModel):
    solved_count: int
    total_count: int
