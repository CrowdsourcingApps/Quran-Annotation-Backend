import ast
from datetime import date
from typing import List, Tuple, Union

from tortoise import Tortoise

from src.models import LabelEnum, Task, User, ValidateCorrectnessTUser
from src.settings import settings
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
    priority_mapping = ast.literal_eval(settings.PRIORITY_MAPPING)

    # Generate the CASE statement dynamically
    case_statement = 'CASE '
    for surra_number, priority in priority_mapping.items():
        case_statement += f'WHEN surra_number = {surra_number}'
        case_statement += f' THEN {priority} '
    case_statement += 'END AS priority'

    # Convert skip_ids to a comma-separated string
    skip_ids_str = ','.join(str(id) for id in skip_ids)

    # Construct the SQL query
    query = f"""
    SELECT DISTINCT on (aya_number, priority)*, {case_statement}
    FROM task
    WHERE label is null
    {f"AND id NOT IN ({skip_ids_str})" if skip_ids_str else ""}
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


async def get_total_tasks(surra_id: int = None):
    if surra_id is not None:
        total_count = await Task.filter(surra_number=surra_id).count()
    else:
        total_count = await Task.all().count()
    return total_count


async def get_total_solved_tasks(surra_id: int = None):
    if surra_id is not None:
        solved_count = await Task.filter(label__not_isnull=True,
                                         surra_number=surra_id
                                         ).count()
    else:
        solved_count = await Task.filter(label__not_isnull=True).count()
    return solved_count


async def get_contribution_by_date(user_id: int, date):
    date_str = date.strftime('%Y-%m-%d')
    query = f"""
    SELECT count(*) FROM validate_correctness_t_user
    WHERE DATE(create_date) = '{date_str}'
    AND user_id = {user_id}
    """
    result = await Tortoise.get_connection('default').execute_query_dict(query)
    count = result[0]['count']
    return count


async def get_users_tokens_with_no_contributions_today(
) -> Tuple[str, str]:
    today = date.today()
    date_str = today.strftime('%Y-%m-%d')
    query = f"""
        select u.language , t.token
        FROM notificationtoken t
        LEFT JOIN "user" u
        ON u.id = t.user_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM validate_correctness_t_user vc
            WHERE vc.user_id = u.id
            AND DATE(create_date) = '{date_str}'
        )
    """
    result = await Tortoise.get_connection('default').execute_query_dict(query)
    return result
