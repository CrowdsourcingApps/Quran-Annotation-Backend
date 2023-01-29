from fastapi import APIRouter, FastAPI

from src.routes.auth import views as auth_views

api_router = APIRouter()
api_router.include_router(auth_views.router, tags=['Authentication'])
# api_router.include_router(control_tasks_views.router,
#                           tags=['Control tasks'],
#                           prefix='/control_tasks',
#                           dependencies=[Depends(firebase_authentication)])


def init_api(app: FastAPI) -> None:
    app.include_router(api_router)
