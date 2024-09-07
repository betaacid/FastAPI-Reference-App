from unittest.mock import patch


@patch("app.routers.characters_router.add_new_character")
def test_create_character_valid_data(
    mock_add_new_character, client, mock_star_wars_character_read
):
    # Given
    character_input_data = {
        "name": "Darth Vader",
    }

    mock_add_new_character.return_value = mock_star_wars_character_read

    # When
    response = client.post("/characters/", json=character_input_data)

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": mock_star_wars_character_read.id,
        "name": mock_star_wars_character_read.name,
        "height": mock_star_wars_character_read.height,
        "mass": None,
    }


def test_create_character_invalid_data(client):
    # Given
    invalid_character_data = {
        "name": 2,
    }

    # When
    response = client.post("/characters/", json=invalid_character_data)

    # Then
    assert response.status_code == 422
    assert "detail" in response.json()
