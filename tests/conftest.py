import pytest
from fastapi.testclient import TestClient
from app.schemas.swapi_character_schema import SwapiCharacter
from main import app
from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from mock_alchemy.mocking import UnifiedAlchemyMagicMock


@pytest.fixture(scope="function")
def mock_db_session():
    return UnifiedAlchemyMagicMock()


@pytest.fixture(scope="function")
def client():
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
