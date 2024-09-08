from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# Happy path: Test successful character creation
def test_create_character_happy_path():
    # Given
    character_data = {"name": "Luke Skywalker"}

    # When
    response = client.post("/characters/", json=character_data)

    # Then
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert "name" in response_data
    assert "height" in response_data
    assert "mass" in response_data


# Character not found path
def test_create_character_not_found():
    # Given
    non_existent_character_data = {"name": "Unknown Character"}

    # When
    response = client.post("/characters/", json=non_existent_character_data)

    # Then
    assert response.status_code == 404
