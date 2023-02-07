from typing import List

from src.models import ValidateCorrectnessCT
from src.routes.control_tasks.validate_correctness.handler import (
    get_validate_correctness_control_task,
    get_validate_correctness_control_task_answer)
from src.routes.control_tasks.validate_correctness.helper import \
    calculate_validate_correctness_MCC
from src.routes.tasks.validate_correctness.handler import (
    get_vctask_labels, update_validate_correctness_task_label)
from src.routes.tasks.validate_correctness.schema import \
    ValidateCorrectnessTOutSchema as VCTOut
from src.settings import settings

BUCKET_PATH = settings.get_minio_Bucket_url()


async def get_validate_correctness_ct(skip_ids: List[int]
                                      ) -> ValidateCorrectnessCT:
    control_task = await get_validate_correctness_control_task(
        golden=True, skip_ids=skip_ids)
    if control_task is None:
        control_task = await get_validate_correctness_control_task(
            golden=False, skip_ids=skip_ids)
    return control_task


def get_whole_path_for_audio_file_name(tasksout):
    for i, obj in enumerate(tasksout):
        tasksout[i].audio_file_name = (
            BUCKET_PATH + obj.audio_file_name
        )
    return tasksout


def convert_schema_list(tasksout: list, control_task: bool) -> List[VCTOut]:
    for i, obj in enumerate(tasksout):
        tasksout[i] = convert_schema(obj, control_task)
    return tasksout


def convert_schema(task, control_task: bool) -> VCTOut:
    return VCTOut(id=task.id,
                  surra_number=task.surra_number,
                  aya_number=task.aya_number,
                  audio_file_name=task.audio_file_name,
                  duration_ms=task.duration_ms,
                  control_task=control_task)


async def check_task_status(task_id: int):
    """ check if the task is solved and ready to the next phase"""
    # fetch each label and user id for the task
    records = await get_vctask_labels(task_id)
    # check if the task has at least three labels
    if len(records) >= 3:
        labels = {}
        max_accuracy = 0
        for record in records:
            label = record.label
            user = await record.user.get()
            # calculate user_metric accuracy in validate correctness task
            control_tasks = await get_validate_correctness_control_task_answer(
                user=user)
            y_true = [await task.user.get().label for task in control_tasks]
            y_pred = [task.label for task in control_tasks]
            user_metric = await calculate_validate_correctness_MCC(y_true,
                                                                   y_pred)
            if label in labels:
                labels[label]['sum_metric'] += user_metric
                labels[label]['annotators_num'] += 1
            else:
                labels[label] = {
                    'sum_metric': user_metric,
                    'annotators_num': 1
                }
            if labels[label]['sum_metric'] > max_accuracy:
                max_accuracy = labels[label]['sum_metric']
        # determine the majority label
        majority_label = [k for k, v in labels.items()
                          if v['sum_metric'] == max_accuracy]
        if len(majority_label) == 1:
            # check if the majority label is 'correct' to have 3 annotators
            final_label = majority_label[0]
            if final_label == 'correct':
                if labels[majority_label[0]]['annotators_num'] < 3:
                    # the task is not solved yet and we need more annotators
                    return
                else:
                    # check the inter-annotator agreement to see if we can
                    # convert the task to control task.
                    pass
            # the task is solved. Update the task label
            await update_validate_correctness_task_label(task_id, final_label)
            return
    # the task is not solved yet and we need more annotators
    return
