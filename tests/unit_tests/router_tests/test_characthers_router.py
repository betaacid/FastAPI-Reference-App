from unittest.mock import MagicMock

from fastapi import HTTPException

from app.dependencies import get_characters_service
from app.errors.custom_exceptions import CharacterNotFoundError
from app.services.characters_service import CharactersService
from main import app


def test_create_character_valid_data(client, mock_star_wars_character_read):
    mock_service = MagicMock(spec=CharactersService)
    mock_service.add_new_character.return_value = mock_star_wars_character_read
    app.dependency_overrides[get_characters_service] = lambda: mock_service

    response = client.post("/characters/", json={"name": "Darth Vader"})

    assert response.status_code == 200
    assert response.json() == {
        "id": mock_star_wars_character_read.id,
        "name": mock_star_wars_character_read.name,
        "height": mock_star_wars_character_read.height,
        "mass": mock_star_wars_character_read.mass,
        "force": mock_star_wars_character_read.force,
    }


def test_create_character_character_not_found(client):
    mock_service = MagicMock(spec=CharactersService)
    mock_service.add_new_character.side_effect = CharacterNotFoundError(
        "Character not found"
    )
    app.dependency_overrides[get_characters_service] = lambda: mock_service

    response = client.post("/characters/", json={"name": "Unknown Character"})

    assert response.status_code == 404


def test_create_character_external_service_error(client):
    mock_service = MagicMock(spec=CharactersService)
    mock_service.add_new_character.side_effect = HTTPException(
        status_code=503,
        detail="External service unavailable. Please try again later.",
    )
    app.dependency_overrides[get_characters_service] = lambda: mock_service

    response = client.post("/characters/", json={"name": "Leia Organa"})

    assert response.status_code == 503


def test_create_character_internal_server_error(client):
    mock_service = MagicMock(spec=CharactersService)
    mock_service.add_new_character.side_effect = HTTPException(
        status_code=500,
        detail="Internal server error. Please try again later.",
    )
    app.dependency_overrides[get_characters_service] = lambda: mock_service

    response = client.post("/characters/", json={"name": "Leia Organa"})

    assert response.status_code == 500


def test_create_character_invalid_data(client):
    mock_service = MagicMock(spec=CharactersService)
    app.dependency_overrides[get_characters_service] = lambda: mock_service

    response = client.post("/characters/", json={"name": 2})

    assert response.status_code == 422
    assert "detail" in response.json()
