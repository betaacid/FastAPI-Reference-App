from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.schemas.swapi_character_schema import SwapiCharacter
from database import get_db_session
from main import app


@pytest.fixture(scope="function")
def mock_db_session():
    # AsyncSession.add is sync; the I/O methods are coroutines
    session = MagicMock()
    session.flush = AsyncMock()
    session.get = AsyncMock()
    return session


@pytest.fixture(scope="function")
def client(mock_db_session):
    # Unit tests never touch a real database, so hand the app a mock session
    # instead of letting get_db_session create an engine
    async def override_get_db_session():
        yield mock_db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def mock_star_wars_character_create() -> StarWarsCharacterCreate:
    return StarWarsCharacterCreate(
        name="Leia Organa",
    )


@pytest.fixture(scope="function")
def mock_swapi_character() -> SwapiCharacter:
    return SwapiCharacter(
        name="Leia Organa",
        height="150",
        mass="49",
    )


@pytest.fixture(scope="function")
def mock_star_wars_character_read() -> StarWarsCharacterRead:
    return StarWarsCharacterRead(
        id=1,
        name="Darth Vader",
        height="123",
        mass="136",
        force=100,
    )


@pytest.fixture
def mock_swapi_response():
    return {
        "count": 1,
        "results": [
            {
                "name": "Darth Vader",
                "height": "202",
                "mass": "136",
            }
        ],
    }
