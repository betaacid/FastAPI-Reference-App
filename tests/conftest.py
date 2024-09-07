import pytest
from fastapi.testclient import TestClient
from main import app
from app.schemas.star_wars_character import StarWarsCharacterRead


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def mock_star_wars_character_read():
    return StarWarsCharacterRead(
        id=1,
        name="Darth Vader",
        rating=202,
        height="123",
    )
