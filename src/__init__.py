from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.database import engine
from src.settings.logging import logger

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as ex:
        logger.exception('[SQLAlchemy] - Error:'
                         f' {ex}')
        db.rollback()
        raise
    finally:
        db.close()
