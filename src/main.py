import secrets
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database import init_db
from src.routes import init_api
from src.routes.notifications.helper import check_and_delete_stale_token
from src.routes.tasks.validate_correctness.notification import (
    achievement_notification, contribute_notification)
from src.settings.logging import logger

app = FastAPI()


def get_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.start()
    return scheduler


@app.on_event('startup')
async def startup_event():
    scheduler = get_scheduler()

    trigger = CronTrigger(hour=12)  # Schedule job to run at midnight
    scheduler.add_job(achievement_notification, trigger=trigger)

    # Set up the interval trigger for every 2 days
    trigger = IntervalTrigger(days=2)
    scheduler.add_job(check_and_delete_stale_token, trigger=trigger)

    trigger = CronTrigger(hour=20)  # Schedule job to run at 8 PM
    scheduler.add_job(contribute_notification, trigger=trigger)


@app.middleware('http')
async def log_requests(request, call_next):
    # do not register healthcheck
    health_check = request.url.path.__contains__('docs')
    if not health_check:
        idem = secrets.token_hex(3)
        logger.info(f'rid={idem} start - "{request.method}" '
                    f'"{request.url.path}"')
        start_time = time.time()

    response = await call_next(request)

    if not health_check:
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f'rid={idem} completed_in={formatted_process_time}ms'
                    f' status_code={response.status_code}')
    return response


origins = [
    'http://localhost',
    'http://localhost:8000',
    'http://www.quranvoice.live/',
    'https://www.quranvoice.live/',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


init_api(app)
init_db(app)
