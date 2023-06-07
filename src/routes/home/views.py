from typing import Optional

from fastapi import APIRouter

from src.routes.home.schema import Statistics
from src.routes.tasks.validate_correctness.handler import (
    get_total_solved_tasks, get_total_tasks)

router = APIRouter()


@router.get('/statistics/validate_correctness',
            status_code=200,
            response_model=Statistics,
            responses={400: {'description': 'BAD REQUEST'}})
async def get_statistics(surra_id: Optional[str] = None):
    """This method bring statistics about all the data we have or
    for a specifc surah in validate correctness tasks"""
    total_count = await get_total_tasks(surra_id=surra_id)
    solved_count = await get_total_solved_tasks(surra_id=surra_id)
    return Statistics(
        solved_count=solved_count,
        total_count=total_count
    )
