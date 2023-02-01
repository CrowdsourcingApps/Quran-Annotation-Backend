
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.models import UserRoleEnum
from src.routes.auth.handler import get_current_user
from src.routes.control_tasks.schema import CreateResponse
from src.routes.control_tasks.validate_correctness import handler
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessCTInSchema

router = APIRouter()
ENTRANCE_EXAM_NO = 7
ALLOWED_ATTEMPTS = 5
VALIDATE_CORRECTNESS_THRESHOLD = 0.7


@router.post('/validate_correctness',
             status_code=200,
             response_model=CreateResponse,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'},
                        403: {'description': 'Forbidden'}})
async def add_validate_correctness_control_tasks(
        control_tasks: List[ValidateCorrectnessCTInSchema],
        user=Depends(get_current_user)) -> list:
    """This method allows Admin to add list of control tasks related to
       validate correctness task type"""
    #  check that user is admin
    if user.user_role != UserRoleEnum.Admin:
        raise HTTPException(status_code=403, detail='you are not authorized')
    result = await handler.Add_validate_correctness_control_tasks_list(
        control_tasks)
    if len(result) < len(control_tasks):
        return CreateResponse(message='Data was uploaded successfully.'
                                      ' Please upload audio files'
                                      'to MinIO control-task-bucket',
                                      errors=result)
    else:
        response = CreateResponse(message='Data was not uploaded successfully',
                                  errors=result)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.dict(),
        )
