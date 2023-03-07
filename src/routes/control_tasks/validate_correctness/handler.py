from typing import List, Union

from src.models import (LabelEnum, User, ValidateCorrectnessCT,
                        ValidateCorrectnessCTUser)
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessCTInSchema
from src.routes.schema import CreationError
from src.settings.logging import logger


async def create_vcct(vcct: ValidateCorrectnessCT
                      ) -> Union[ValidateCorrectnessCT, str]:
    try:
        vcct_obj = await ValidateCorrectnessCT.create(
            surra_number=vcct.surra_number,
            aya_number=vcct.aya_number,
            client_id=vcct.client_id,
            audio_file_name=vcct.audio_file_name,
            duration_ms=vcct.duration_ms,
            label=vcct.label,
            golden=vcct.golden,
        )
        return vcct_obj
    except Exception as ex:
        logger.exception('[db] - Add new ValidateCorrectnessControlTask'
                         f'item error: {ex}')
        error_message = str(ex)
        return error_message


async def Add_validate_correctness_control_tasks_list(
        list: List[ValidateCorrectnessCTInSchema]) -> List[CreationError]:
    errors: List[CreationError] = []
    for control_task in list:
        result = await create_vcct(control_task)
        if isinstance(result, str):
            error = CreationError(message=result,
                                  item=control_task.audio_file_name)
            errors.append(error)
    return errors


async def get_previous_solved_questions(user: User) -> List[int]:
    """ get ids list of validate correctness solved questions"""
    ids = await user.validate_correctness_cts.filter().only('id').all()
    return ids


async def get_validate_correctness_list(
    golden: bool,
    skip_ids: List[int]
) -> List[ValidateCorrectnessCT]:
    """ get list of validate correctness control tasks"""
    vcct = await ValidateCorrectnessCT.filter(
        golden=golden,
        id__not_in=skip_ids
    ).all()
    return vcct


async def get_validate_correctness_control_task_by_id(
        id: int) -> ValidateCorrectnessCT:
    """ get validate correctness control task"""
    vcct = await ValidateCorrectnessCT.get(id=id)
    return vcct


async def get_validate_correctness_control_task(
        golden: bool, skip_ids: List[int]) -> ValidateCorrectnessCT:
    """ get validate correctness control task"""
    vcct = await ValidateCorrectnessCT.filter(
        golden=golden,
        id__not_in=skip_ids
    ).first()
    return vcct


async def save_validate_correctness_control_task_answer(
        user: User,
        task: ValidateCorrectnessCT,
        answer: LabelEnum,
        test: bool,
        correct: bool) -> Union[ValidateCorrectnessCTUser, str]:
    """ save the answer of validate correctness control task"""
    try:
        vctu = await ValidateCorrectnessCTUser.create(
            user=user,
            validatecorrectnessct=task,
            label=answer,
            test=test,
            correct_answer=correct)
        return vctu
    except Exception as ex:
        logger.exception('[db] - Add new ValidateCorrectnessCTUser'
                         f'item error: {ex}')
        error_message = str(ex)
        return error_message


async def get_validate_correctness_control_task_answer(
        user: User) -> List[ValidateCorrectnessCTUser]:
    """ get the answers for validate correctness control task
        of specific user"""
    vcctu_list = await ValidateCorrectnessCTUser.filter(
        user=user,
        test=False
    ).all()
    vcctu_list_test = await ValidateCorrectnessCTUser.filter(
        user=user,
        test=True
    ).order_by('-create_date').limit(7).all()
    vcctu_list.extend(vcctu_list_test)
    return vcctu_list
