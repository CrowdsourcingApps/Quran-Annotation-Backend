from sqlalchemy import create_engine

from src.settings import settings

DATABASE_URL = (f'postgresql+psycopg2://{settings.DB_USER}:'
                f'{settings.DB_PASSWORD}@{settings.DB_HOST}'
                f':5432/{settings.DB_NAME}')
engine = create_engine(DATABASE_URL)
