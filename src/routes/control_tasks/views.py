
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.models import User, UserRoleEnum
from src.routes.auth.handler import (
    get_current_user, update_validate_correctness_exam_correct_no)
from src.routes.control_tasks.schema import CreateResponse, CreationError
from src.routes.control_tasks.validate_correctness import handler
from src.routes.control_tasks.validate_correctness.helper import \
    get_validate_correctness_entrance_exam_list
from src.routes.control_tasks.validate_correctness.schema import (
    ValidateCorrectnessCTInSchema, ValidateCorrectnessCTOutSchema,
    ValidateCorrectnessExamAnswers)

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
        user: User = Depends(get_current_user)) -> list:
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
                                      ' to MinIO control-task-bucket',
                                      errors=result)
    else:
        response = CreateResponse(message='Data was not uploaded successfully',
                                  errors=result)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.dict(),
        )


@router.get('/validate_correctness',
            response_model=List[ValidateCorrectnessCTOutSchema],
            status_code=200,
            responses={401: {'description': 'UNAUTHORIZED'},
                       404: {'description': 'NOT FOUND'},
                       400: {'description': 'BAD REQUEST'}
                       })
async def get_validate_correctness_entrance_exam(
        user: User = Depends(get_current_user)) -> list:
    """ get 7 real like tasks to test if the annotator is qualified to
        participate"""
    # validation
    # the user hasn't pass the test related to validate correctness task
    pass_exam = user.validate_correctness_exam_correct_no > 0
    if pass_exam:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Participant already pass the entrance exam',
        )
    # the user can take the test if number of attempts less than five
    # => 7 questions * 5 attempts = 35 questions
    questions_no = ENTRANCE_EXAM_NO*ALLOWED_ATTEMPTS
    # take previous solved questions in case user tried before and didn't pass
    ps_questions = await handler.get_previous_solved_questions(user)
    ps_questions_ids = [ps_question.id for ps_question in ps_questions]
    ps_questions_count = len(ps_questions_ids)
    if ps_questions_count >= questions_no:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Participant not allowed to attempt more than 5 times',
        )

    control_tasks = await get_validate_correctness_entrance_exam_list(
        ps_questions_ids)
    if control_tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No tasks available for entrance test',
        )
    # case of remain questions less than 7
    if len(control_tasks) < ENTRANCE_EXAM_NO:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No tasks available for entrance test. please try later',
        )
    return control_tasks


@router.post('/validate_correctness/answers',
             status_code=200,
             response_model=CreateResponse,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'}})
async def add_validate_correctness_entrance_exam_answers(
        exam_answers: List[ValidateCorrectnessExamAnswers],
        user=Depends(get_current_user)) -> list:
    """This method allows to calculate accuracy of the user and determine
     if they pass or fail"""
    # validation
    # the user hasn't pass the test related to validate correctness task
    pass_exam = user.validate_correctness_exam_correct_no > 0
    if pass_exam:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Participant already pass the entrance exam',
        )

    if len(exam_answers) != ENTRANCE_EXAM_NO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participant's answers should be equal to"
                   f' {ENTRANCE_EXAM_NO}',
        )
    # calculate number of correct
    correct_answers = 0
    errors: List[CreationError] = []
    for exam_answer in exam_answers:
        task = await handler.get_validate_correctness_control_task(
            id=exam_answer.ct_id)
        result = await handler.save_validate_correctness_control_task_answer(
            user, task, exam_answer.label, test=True)
        if isinstance(result, str):
            error = CreationError(message=result,
                                  item=exam_answer.ct_id)
            errors.append(error)
        if task.label == exam_answer.label:
            correct_answers += 1
    user_accuracy = correct_answers/ENTRANCE_EXAM_NO
    # update user data for accuracy if the user pass the test
    if len(errors) == 0 and user_accuracy >= VALIDATE_CORRECTNESS_THRESHOLD:
        await update_validate_correctness_exam_correct_no(
            user.id,
            correct_answers)
    if len(errors) < ENTRANCE_EXAM_NO:
        return CreateResponse(
            message='Data was uploaded successfully.',
            errors=errors)
    else:
        response = CreateResponse(message='Data was not uploaded successfully',
                                  errors=errors)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.dict()
        )