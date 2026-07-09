from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

from app.errors.custom_exceptions import CharacterNotFoundError


@patch("app.services.characters_service.add_new_character", new_callable=AsyncMock)
def test_create_character_valid_data(
    mock_add_new_character, client, mock_star_wars_character_read
):
    mock_add_new_character.return_value = mock_star_wars_character_read

    response = client.post("/characters/", json={"name": "Darth Vader"})

    assert response.status_code == 200
    assert response.json() == {
        "id": mock_star_wars_character_read.id,
        "name": mock_star_wars_character_read.name,
        "height": mock_star_wars_character_read.height,
        "mass": mock_star_wars_character_read.mass,
        "force": mock_star_wars_character_read.force,
    }


@patch("app.services.characters_service.add_new_character", new_callable=AsyncMock)
def test_create_character_character_not_found(mock_add_new_character, client):
    mock_add_new_character.side_effect = CharacterNotFoundError("Character not found")

    response = client.post("/characters/", json={"name": "Unknown Character"})

    assert response.status_code == 404


@patch("app.services.characters_service.add_new_character", new_callable=AsyncMock)
def test_create_character_external_service_error(mock_add_new_character, client):
    mock_add_new_character.side_effect = HTTPException(
        status_code=503,
        detail="External service unavailable. Please try again later.",
    )

    response = client.post("/characters/", json={"name": "Leia Organa"})

    assert response.status_code == 503


@patch("app.services.characters_service.add_new_character", new_callable=AsyncMock)
def test_create_character_internal_server_error(mock_add_new_character, client):
    mock_add_new_character.side_effect = HTTPException(
        status_code=500,
        detail="Internal server error. Please try again later.",
    )

    response = client.post("/characters/", json={"name": "Leia Organa"})

    assert response.status_code == 500


def test_create_character_invalid_data(client):
    response = client.post("/characters/", json={"name": 2})

    assert response.status_code == 422
    assert "detail" in response.json()
