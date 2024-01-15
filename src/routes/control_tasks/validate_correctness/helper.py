import random
from typing import List, Tuple, Union

from sklearn.metrics import accuracy_score, matthews_corrcoef

from src.models import LabelEnum, User, ValidateCorrectnessCT
from src.routes.control_tasks.validate_correctness.handler import (
    get_validate_correctness_control_task_answer,
    get_validate_correctness_control_task_by_id, get_validate_correctness_list,
    save_validate_correctness_control_task_answer)
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessExamAnswers
from src.routes.control_tasks.validate_correctness.schema import \
    VCCTInSchema as VCCTIn
from src.routes.control_tasks.validate_correctness.schema import \
    VCCTOutSchema as VCCTOut
from src.routes.schema import CreationError
from src.settings import settings
from src.settings.logging import logger

BUCKET_PATH = settings.get_audio_url()
ENTRANCE_EXAM_NO = 8


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
        ct_type6 = [item for item in golden_tasks
                    if item.label == LabelEnum.InComplete]
        test_questions = []
        test_questions += random.sample(ct_type1, k=2)
        test_questions += random.sample(ct_type2, k=2)
        test_questions += random.sample(ct_type3, k=1)
        test_questions += random.sample(ct_type4, k=1)
        test_questions += random.sample(ct_type5, k=1)
        test_questions += random.sample(ct_type6, k=1)
        random.shuffle(test_questions)
        try:
            # add the whole path for the file name
            tasks = []
            for i, obj in enumerate(test_questions):
                reason = await obj.golden_reason
                tasks.append(VCCTOut(
                    id=obj.id,
                    surra_number=obj.surra_number,
                    aya_number=obj.aya_number,
                    audio_file_name=(
                        BUCKET_PATH + obj.audio_file_name
                    ),
                    duration_ms=obj.duration_ms,
                    label=obj.label,
                    reason_ar=reason[0].reason_ar if len(reason) > 0 else None,
                    reason_en=reason[0].reason_en if len(reason) > 0 else None,
                    reason_ru=reason[0].reason_ru if len(reason) > 0 else None
                ))
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
    errors: List[CreationError] = []
    y_pred = [task.label for task in answers]
    y_true = []
    for answer in answers:
        task = await get_validate_correctness_control_task_by_id(
            id=answer.id)
        if task is None:
            error = CreationError(message='control task not found',
                                  item=task.id)
            errors.append(error)
            continue
        y_true.append(task.label)
        if task.label == answer.label:
            correct = True
        else:
            correct = False
        result = await save_validate_correctness_control_task_answer(
            user, task, answer.label, test=test, correct=correct)
        if isinstance(result, str):
            error = CreationError(message=result,
                                  item=answer.id)
            errors.append(error)
    user_metric = 0
    if len(errors) == 0:
        user_metric = await calculate_validate_correctness_MCC(y_true, y_pred)
    return errors, user_metric


def convert_schema(control_task: VCCTIn) -> ValidateCorrectnessCT:
    """ Conver control task entered by admin to the standard model"""
    return ValidateCorrectnessCT(
        surra_number=control_task.surra_number,
        aya_number=control_task.aya_number,
        client_id=control_task.client_id,
        audio_file_name=control_task.audio_file_name,
        duration_ms=control_task.duration_ms,
        label=control_task.label,
        golden=True)


def convert_schema_list(control_task_list: List[VCCTIn]
                        ) -> List[ValidateCorrectnessCT]:
    """ Conver control task entered by admin to the standard model"""
    for i, obj in enumerate(control_task_list):
        control_task_list[i] = convert_schema(obj)
    return control_task_list


async def calculate_validate_correctness_MCC(y_true, y_pred) -> float:
    class_weights = {'correct': 2, 'in_correct': 2, 'not_related_quran': 1,
                     'not_match_aya': 1, 'multiple_aya': 1, 'in_complete': 1}
    sample_weight = [class_weights[y] for y in y_true]
    mcc = matthews_corrcoef(y_true, y_pred, sample_weight=sample_weight)
    return mcc


async def calculate_validate_correctness_acc(y_true, y_pred) -> float:
    acc = accuracy_score(y_true, y_pred)
    return acc


async def get_y_true_y_predict_user(user: User) -> Tuple[list, list]:
    control_tasks = await get_validate_correctness_control_task_answer(
        user=user)
    y_true = []
    for task in control_tasks:
        task = await task.validatecorrectnessct.get()
        y_true.append(task.label)
    y_pred = [task.label for task in control_tasks]
    return y_true, y_pred


async def get_vc_user_accuracy(user: User) -> float:
    """ Get user accuracy value between 0 and 1"""
    y_true, y_pred = await get_y_true_y_predict_user(user=user)
    if len(y_true) == 0:
        acc = 0
    else:
        acc = await calculate_validate_correctness_acc(y_true, y_pred)
    return acc
