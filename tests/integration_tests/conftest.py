import pytest
from dotenv import load_dotenv

load_dotenv()

import os
from typing import AsyncIterator

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from database import get_db_session
from main import app


@pytest.fixture
def integration_client():
    # A dedicated NullPool engine per test: each TestClient runs its own event
    # loop, and pooled asyncpg connections cannot cross loops.
    engine = create_async_engine(os.getenv("DATABASE_URL"), poolclass=NullPool)

    async def override_get_db_session() -> AsyncIterator[AsyncSession]:
        session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
        session = session_factory()
        try:
            yield session
            # roll back instead of committing so tests leave no data behind
            await session.rollback()
        finally:
            await session.close()

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
