def test_create_character_happy_path(integration_client):
    response = integration_client.post("/characters/", json={"name": "Luke Skywalker"})

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert "name" in response_data
    assert "height" in response_data
    assert "mass" in response_data


def test_create_character_not_found(integration_client):
    response = integration_client.post(
        "/characters/", json={"name": "Unknown Character"}
    )

    assert response.status_code == 404
