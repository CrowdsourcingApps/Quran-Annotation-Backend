from typing import List, Union

from tortoise import Tortoise

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
    # vctts = await Task.filter(id__not_in=skip_ids,
    #                          label=None).order_by('id').limit(limit).all()
    priority_mapping = {
        1: 1,
        112: 2,
        114: 3,
        2255: 4,
        999008: 5,
        109: 6,
        113: 7,
        103: 8,
        108: 9,
        999001: 10,
        111: 11,
        110: 12,
        999003: 13,
        999002: 14,
        104: 15,
        105: 16,
        999005: 17,
        999006: 18,
        2185: 19,
        107: 20,
        106: 21,
        999004:  22,
        999007: 23,
        999009: 24
    }
    # limit_mapping= {
    #     1:8,
    #     97: 5,
    #     103:3,
    #     104:9,
    #     105:5,
    #     106:4,
    #     107:7,
    #     108:3,
    #     109:6,
    #     110:3,
    #     111:5,
    #     112:4,
    #     113:5,
    #     114:6,
    #     2255:7,
    #     2185:4,
    #     999002:3,
    #     999001:5,
    #     999003:6,
    #     999004:10,
    #     999006:5,
    #     999005:20,
    #     999007:10,
    #     999008:12,
    #     999009:10
    # }

    # Generate the CASE statement dynamically
    case_statement = 'CASE '
    for surra_number, priority in priority_mapping.items():
        case_statement += f'WHEN surra_number = {surra_number}'
        case_statement += f' THEN {priority} '
    case_statement += 'END AS priority'

    # Construct the SQL query
    query = f"""
    SELECT DISTINCT on (aya_number, priority)*, {case_statement}
    FROM task
    WHERE label is null
    ORDER BY priority,aya_number,surra_number , id
    LIMIT {limit};
    """
    vcts_dict = await Tortoise.get_connection('default').execute_query_dict(
        query)
    vcts = [Task(**vct_dict) for vct_dict in vcts_dict]
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
