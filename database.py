import os
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

_engine = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(os.getenv("DATABASE_URL"))
    return _engine


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Provide a session scoped to one request.

    The transaction boundary lives here, not in the database clients: the
    session commits once the request handler finishes successfully and rolls
    back if it raises, so a request that writes multiple records stays atomic.
    """
    session_factory = async_sessionmaker(bind=get_engine(), expire_on_commit=False)
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
