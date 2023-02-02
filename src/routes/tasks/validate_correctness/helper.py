from typing import List

from src.models import ValidateCorrectnessCT
from src.routes.control_tasks.validate_correctness.handler import \
    get_validate_correctness_control_task
from src.routes.tasks.validate_correctness.schema import \
    ValidateCorrectnessTOutSchema as VCTOut
from src.settings import settings

BUCKET_PATH = (
    settings.MINIO_SERVER+'/'+settings.MINIO_BUCKET_NAME+'/'
)


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
