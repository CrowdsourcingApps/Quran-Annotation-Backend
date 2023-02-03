import random
from typing import List, Tuple, Union

from src.models import LabelEnum, User
from src.routes.control_tasks.validate_correctness.handler import (
    get_validate_correctness_control_task_by_id, get_validate_correctness_list,
    save_validate_correctness_control_task_answer)
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessCTOutSchema as VCCTOut
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessExamAnswers
from src.routes.schema import CreationError
from src.settings import settings
from src.settings.logging import logger

BUCKET_PATH = settings.get_minio_Bucket_url()


async def get_validate_correctness_entrance_exam_list(
        previous_solved_questions: List[int]) -> Union[List[VCCTOut], None]:
    try:
        golden_tasks = await get_validate_correctness_list(
            golden=True, skip_ids=previous_solved_questions)
        ct_type1 = [item for item in golden_tasks
                    if item.label == LabelEnum.Correct]
        ct_type2 = [item for item in golden_tasks
                    if item.label == LabelEnum.InCorrect]
        ct_type3 = [item for item in golden_tasks
                    if item.label == LabelEnum.MultipleAya]
        ct_type4 = [item for item in golden_tasks
                    if item.label == LabelEnum.NotMatchAya]
        ct_type5 = [item for item in golden_tasks
                    if item.label == LabelEnum.NotRelatedToQuran]
        test_questions = []
        test_questions += random.sample(ct_type1, k=2)
        test_questions += random.sample(ct_type2, k=2)
        test_questions += random.sample(ct_type3, k=1)
        test_questions += random.sample(ct_type4, k=1)
        test_questions += random.sample(ct_type5, k=1)
        random.shuffle(test_questions)
        try:
            # add the whole path for the file name
            for i, obj in enumerate(test_questions):
                test_questions[i].audio_file_name = (
                    BUCKET_PATH + obj.audio_file_name
                )
            tasks = [await VCCTOut.from_tortoise_orm(task)
                     for task in test_questions]
            return tasks
        except Exception as ex:
            logger.exception('Parsing VCCT list to'
                             f' VCCTOut list error: {ex}')
            return None
    except Exception as ex:
        logger.exception('[db] - get contol tasks from validate '
                         f'correctness control tasks table error: {ex}')
        return None


async def save_validate_control_tasks_list(
        answers: ValidateCorrectnessExamAnswers,
        user: User,
        test: bool) -> Tuple[List[CreationError], int]:
    correct_answers = 0
    correct = False
    errors: List[CreationError] = []
    for answer in answers:
        task = await get_validate_correctness_control_task_by_id(
            id=answer.id)
        if task is None:
            error = CreationError(message='control task not found',
                                  item=task.id)
            errors.append(error)
            continue
        if task.label == answer.label:
            correct_answers += 1
            correct = True
        else:
            correct = False
        result = await save_validate_correctness_control_task_answer(
            user, task, answer.label, test=test, correct=correct)
        if isinstance(result, str):
            error = CreationError(message=result,
                                  item=answer.id)
            errors.append(error)
    return errors, correct_answers
