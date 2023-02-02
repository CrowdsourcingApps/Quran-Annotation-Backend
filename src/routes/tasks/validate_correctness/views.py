from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.models import User
from src.routes.auth.handler import get_current_user
from src.routes.control_tasks.validate_correctness.handler import \
    get_previous_solved_questions
from src.routes.tasks.validate_correctness import handler, helper
from src.routes.tasks.validate_correctness.schema import \
    ValidateCorrectnessTOutSchema as VCTOut

router = APIRouter(prefix='/validate_correctness')
TASKS_In_BATCH_NO = 5
REAL_TASKS_NO = 4


@router.get('/',
            response_model=List[VCTOut],
            status_code=200,
            responses={401: {'description': 'UNAUTHORIZED'},
                       404: {'description': 'NOT FOUND'},
                       400: {'description': 'BAD REQUEST'}
                       })
async def get_validate_correctness_tasks(
        user: User = Depends(get_current_user)) -> list:
    """ get real tasks for annotator to solve"""
    #  check that user is qualified
    pass_exam = user.validate_correctness_exam_correct_no > 0
    if not pass_exam:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Participant should pass the entrance exam first',
        )
    # fetch N real tasks
    ps_questions = await handler.get_previous_solved_questions(user)
    ps_questions_ids = [ps_question.id for ps_question in ps_questions]
    tasks = await handler.get_validate_correctness_tasks(REAL_TASKS_NO,
                                                         ps_questions_ids)
    if len(tasks) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No more tasks to solve',
        )

    # fetch one control tasks
    ps_ct_questions = await get_previous_solved_questions(user)
    ps_ct_questions_ids = [ps_question.id for ps_question in ps_ct_questions]
    control_task = await helper.get_validate_correctness_ct(
        ps_ct_questions_ids)

    # convert them to output schema
    tasksout = helper.convert_schema_list(tasks, control_task=False)
    control_task_out = helper.convert_schema_list([control_task],
                                                  control_task=True)
    tasksout.extend(control_task_out)
    tasksout = helper.get_whole_path_for_audio_file_name(tasksout)
    return tasksout
