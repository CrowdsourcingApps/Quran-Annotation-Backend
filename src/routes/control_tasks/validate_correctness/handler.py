from typing import List, Union

from src.models import ValidateCorrectnessCT
from src.routes.control_tasks.schema import CreationError
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessCTInSchema
from src.settings import settings
from src.settings.logging import logger

TEST_BUCKET_PATH = (
    settings.MINIO_SERVER+'/'+settings.MINIO_TEST_TASKS_BUCKET+'/'
)


async def create_vcct(vcct: ValidateCorrectnessCTInSchema
                      ) -> Union[ValidateCorrectnessCT, str]:
    try:
        vcct_obj = await ValidateCorrectnessCT.create(
            surra_number=vcct.surra_number,
            aya_number=vcct.aya_number,
            audio_file_name=vcct.audio_file_name,
            duration_ms=vcct.duration_ms,
            label=vcct.label)
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
                                  audio=control_task.audio_file_name)
            errors.append(error)
    return errors
