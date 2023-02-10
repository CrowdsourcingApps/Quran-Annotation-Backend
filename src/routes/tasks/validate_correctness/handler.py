from typing import List, Union

from src.models import LabelEnum, Task, User, ValidateCorrectnessTUser
from src.settings.logging import logger


async def get_previous_solved_questions(user: User) -> List[int]:
    """ get ids list of validate correctness solved tasks"""
    ids = await user.validate_correctness_ts.filter().only('id').all()
    return ids


async def get_validate_correctness_task(
        id: int) -> Union[Task, None]:
    """ get validate correctness task"""
    vct = await Task.get_or_none(id=id)
    return vct


async def get_validate_correctness_tasks(
        limit: int, skip_ids: List[int]) -> List[Task]:
    """ get validate correctness tasks"""
    vcts = await Task.filter(id__not_in=skip_ids,
                             label=None).limit(limit).all()
    return vcts


async def store_task_answer(
        user: User,
        task: Task,
        answer: LabelEnum) -> Union[ValidateCorrectnessTUser, str]:
    """ store the answer of validate correctness task"""
    try:
        vctu = await ValidateCorrectnessTUser.create(
            user=user,
            task=task,
            label=answer)
        return vctu
    except Exception as ex:
        logger.exception('[db] - Add new ValidateCorrectnessTUser'
                         f'item error: {ex}')
        error_message = str(ex)
        return error_message


async def get_vctask_labels(task_id: int) -> List[ValidateCorrectnessTUser]:
    """ get labels of validate correctness task"""
    labels = await ValidateCorrectnessTUser.filter(
        task_id=task_id).all()
    return labels


async def update_validate_correctness_task_label(task_id: int,
                                                 mv_label: LabelEnum) -> bool:
    """ update validate correctness task label"""
    result = await Task.filter(id=task_id).update(
        label=mv_label)
    if result == 0:
        logger.exception(f'[db] - update task label failed {task_id} with'
                         f' label {mv_label}')
        return False
    return True
