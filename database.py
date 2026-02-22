import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

Base = declarative_base()

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(os.getenv("DATABASE_URL"))
    return _engine


def get_db_session():
    session_factory = sessionmaker(bind=get_engine())
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
