import asyncio
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.models import User
from src.routes.auth.handler import (get_current_user,
                                     update_user_validate_correctness_tasks_no)
from src.routes.control_tasks.validate_correctness.handler import (
    get_previous_solved_questions, get_solved_control_tasks_by_date)
from src.routes.control_tasks.validate_correctness.helper import \
    save_validate_control_tasks_list
from src.routes.schema import CreateResponse, CreationError
from src.routes.tasks.validate_correctness import handler, helper
from src.routes.tasks.validate_correctness.schema import (
    Contribution, ValidateCorrectnessAnswers)
from src.routes.tasks.validate_correctness.schema import \
    ValidateCorrectnessTOutSchema as VCTOut
from src.settings import settings

router = APIRouter(prefix='/validate_correctness')
TASKS_In_BATCH_NO = 5
REAL_TASKS_NO = settings.REAL_TASKS_NO


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
    pass_exam = user.validate_correctness_exam_pass
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
    if control_task is not None:
        control_task_out = helper.convert_schema_list([control_task],
                                                      control_task=True)
        tasksout.extend(control_task_out)
    tasksout = helper.get_whole_path_for_audio_file_name(tasksout)
    return tasksout


@router.post('/answers',
             status_code=200,
             response_model=CreateResponse,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'}})
async def add_validate_correctness_entrance_exam_answers(
        exam_answers: List[ValidateCorrectnessAnswers],
        user: User = Depends(get_current_user)) -> list:
    """This method allows to calculate accuracy of the user and determine
     if they pass or fail"""
    # validation
    # the user hasn't pass the test related to validate correctness task
    pass_exam = user.validate_correctness_exam_pass
    if not pass_exam:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Participant should pass the entrance exam first',
        )
    # comment this validation for the case of lettel number of tasks left
    # if len(exam_answers) != TASKS_In_BATCH_NO:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Participant's answers should be equal to"
    #                f' {TASKS_In_BATCH_NO}',
    #     )

    ps_questions = await handler.get_previous_solved_questions(user)
    ps_questions_ids = [ps_question.id for ps_question in ps_questions]

    questions_ids = [item.id for item in exam_answers
                     if not item.control_task]

    # Check if all elements of filtered_ids are in ps_questions_ids
    repeated_request = all(id in ps_questions_ids for id in questions_ids)
    if repeated_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The request has already been sent',
        )

    errors: List[CreationError] = []
    real_tasks_answers = [obj for obj in exam_answers if not obj.control_task]
    control_task_answer = [obj for obj in exam_answers if obj.control_task]
    # store answers for real tasks
    for answer in real_tasks_answers:
        # check if the task is exist
        task = await handler.get_validate_correctness_task(id=answer.id)
        if task is None:
            error = CreationError(message='Task not found',
                                  item=task.id)
            errors.append(error)
            continue
        # store answer for real task and update user's accuracy
        result = await handler.store_task_answer(user, task, answer.label)
        if isinstance(result, str):
            error = CreationError(message=result,
                                  item=task.id)
            errors.append(error)
        else:
            # check if the task status is changed and update the
            # label according to the majority of answers
            asyncio.create_task(helper.check_task_status(task.id))

    # # store answer for control task
    # Remove correct_answer property to match input schema of the method
    errors_c, _ = await save_validate_control_tasks_list(
        control_task_answer, user, test=False)
    errors.extend(errors_c)
    # update number of solved tasks for user
    num = len(exam_answers) - len(errors)
    if num > 0:
        update_result = await update_user_validate_correctness_tasks_no(
            user, num)
        if update_result is False:
            error = CreationError(
                message='User validate_correctness_tasks_no was not updated',
                item=user.id)
            errors.append(error)
        return CreateResponse(errors=errors,
                              message='Data was uploaded successfully.')
    return CreateResponse(errors=errors,
                          message='Data was not uploaded successfully.')


@router.get('/today_contribution',
            status_code=200,
            response_model=Contribution,
            responses={400: {'description': 'BAD REQUEST'}})
async def get_today_contribution(user: User = Depends(get_current_user)):
    """This method bring today contribution for the user"""
    # Get today's date
    today = date.today()
    count_control_tasks = await get_solved_control_tasks_by_date(user.id,
                                                                 today)
    count_contribution = await handler.get_contribution_by_date(user.id, today)
    count = count_control_tasks + count_contribution
    return Contribution(
        count=count
    )
