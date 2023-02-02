from typing import List

from src.models import Task, User


async def get_previous_solved_questions(user: User) -> List[int]:
    """ get ids list of validate correctness solved tasks"""
    ids = await user.validate_correctness_ts.filter().only('id').all()
    return ids


async def get_validate_correctness_task(
        id: int) -> Task:
    """ get validate correctness task"""
    vct = await Task.get(id=id)
    return vct


async def get_validate_correctness_tasks(
        limit: int, skip_ids: List[int]) -> List[Task]:
    """ get validate correctness tasks"""
    vcts = await Task.filter(id__not_in=skip_ids,
                             label=None).limit(limit).all()
    return vcts
