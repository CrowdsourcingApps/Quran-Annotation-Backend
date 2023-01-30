from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.settings import settings

DB_URL = (f'postgres://{settings.DB_USER}:'
          f'{settings.DB_PASSWORD}@{settings.DB_HOST}'
          f':5432/{settings.DB_NAME}')
TORTOISE_ORM = {
    'connections': {
        'default': DB_URL,
        'healthcheck': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': settings.DB_HOST,
                'port': 5432,
                'user': settings.DB_USER,
                'password': settings.DB_PASSWORD,
                'database': settings.DB_NAME,
                'timeout': 0.9,
            }
        },
    },
    'apps': {
        'models': {
            'models': ['src.models', 'aerich.models'],
        }
    }
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
