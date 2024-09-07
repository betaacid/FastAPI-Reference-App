import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db_session
from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from mock_alchemy.mocking import UnifiedAlchemyMagicMock


@pytest.fixture(scope="function")
def mock_db_session():
    mock_db = UnifiedAlchemyMagicMock()
    return mock_db


@pytest.fixture(scope="function")
def client(mock_db_session):
    def override_get_db_session():
        yield mock_db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def mock_star_wars_character_create() -> StarWarsCharacterCreate:
    return StarWarsCharacterCreate(
        name="Leia Organa",
        rating=180,
    )


@pytest.fixture(scope="function")
def mock_star_wars_character_read() -> StarWarsCharacterRead:
    return StarWarsCharacterRead(
        id=1,
        name="Darth Vader",
        rating=202,
        height="123",
    )
