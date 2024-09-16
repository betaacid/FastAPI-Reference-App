import pytest
import responses
import requests
from app.clients.networking.swapi_networking_client import (
    get_character_from_swapi,
    transform_swapi_character_json_to_pydantic,
)
from app.schemas.swapi_character_schema import SwapiCharacter
from app.errors.custom_exceptions import CharacterNotFoundError

SWAPI_BASE_URL = "https://swapi.dev/api"


@responses.activate
def test_get_character_from_swapi_success(mock_swapi_response):
    search_url = f"{SWAPI_BASE_URL}/people/?search=vader"
    responses.add(responses.GET, search_url, json=mock_swapi_response, status=200)

    result = get_character_from_swapi("vader")

    assert "results" in result
    assert len(result["results"]) > 0

    character = result["results"][0]
    assert character["name"] == "Darth Vader"
    assert character["height"] == "202"
    assert character["mass"] == "136"

    assert responses.calls[0].request.url == search_url
    assert len(responses.calls) == 1


@responses.activate
def test_get_character_from_swapi_not_found():
    mock_response_data = {"count": 0, "results": []}

    search_url = f"{SWAPI_BASE_URL}/people/?search=unknowncharacter"
    responses.add(responses.GET, search_url, json=mock_response_data, status=200)

    result = get_character_from_swapi("unknowncharacter")

    assert result["count"] == 0
    assert len(result["results"]) == 0

    assert responses.calls[0].request.url == search_url
    assert len(responses.calls) == 1


@responses.activate
def test_get_character_from_swapi_error():
    search_url = f"{SWAPI_BASE_URL}/people/?search=vader"
    responses.add(
        responses.GET, search_url, json={"detail": "Internal Server Error"}, status=500
    )

    with pytest.raises(requests.HTTPError):
        get_character_from_swapi("vader")

    assert responses.calls[0].request.url == search_url
    assert len(responses.calls) == 1


def test_transform_swapi_character_json_to_pydantic_valid(mock_swapi_response):
    # When: The SWAPI response is valid
    result = transform_swapi_character_json_to_pydantic(mock_swapi_response)

    # Then: Ensure the result is a valid SwapiCharacter model
    assert isinstance(result, SwapiCharacter)
    assert result.name == "Darth Vader"
    assert result.height == "202"
    assert result.mass == "136"


def test_transform_swapi_character_json_to_pydantic_no_results():
    # Given: A response with no results
    mock_empty_response = {"count": 0, "results": []}

    # When / Then: Expect a CharacterNotFoundError to be raised
    with pytest.raises(CharacterNotFoundError):
        transform_swapi_character_json_to_pydantic(mock_empty_response)


def test_transform_swapi_character_json_to_pydantic_missing_fields():
    # Given: A response with missing fields (e.g., missing 'mass')
    mock_response_missing_fields = {
        "count": 1,
        "results": [
            {
                "name": "Luke Skywalker",
                "height": "172",
                # 'mass' is missing
            }
        ],
    }

    # When:
    result = transform_swapi_character_json_to_pydantic(mock_response_missing_fields)

    # Then:
    assert isinstance(result, SwapiCharacter)
    assert result.name == "Luke Skywalker"
    assert result.height == "172"
    assert result.mass is None
