from fastapi import APIRouter, Depends, FastAPI

from src.routes.auth import views as auth_views
from src.routes.auth.handler import get_current_user
from src.routes.control_tasks import views as control_tasks_views

api_router = APIRouter()
api_router.include_router(auth_views.router, tags=['Authentication'])
api_router.include_router(control_tasks_views.router,
                          tags=['Control tasks'],
                          prefix='/control_tasks',
                          dependencies=[Depends(get_current_user)])


def init_api(app: FastAPI) -> None:
    app.include_router(api_router)