import httpx
import pytest

from app.clients.networking.swapi_networking_client import (
    SWAPI_BASE_URL,
    SwapiClient,
    transform_swapi_character_json_to_pydantic,
)
from app.errors.custom_exceptions import CharacterNotFoundError, SwapiCharacterError
from app.schemas.swapi_character_schema import SwapiCharacter


def make_swapi_client(handler) -> SwapiClient:
    """Build a SwapiClient whose httpx client never touches the network."""
    transport = httpx.MockTransport(handler)
    return SwapiClient(httpx.AsyncClient(base_url=SWAPI_BASE_URL, transport=transport))


async def test_get_character_from_swapi_success(mock_swapi_response):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/people/"
        assert request.url.params["search"] == "vader"
        return httpx.Response(200, json=mock_swapi_response)

    swapi_client = make_swapi_client(handler)

    result = await swapi_client.get_character("vader")

    assert "results" in result
    assert len(result["results"]) > 0

    character = result["results"][0]
    assert character["name"] == "Darth Vader"
    assert character["height"] == "202"
    assert character["mass"] == "136"


async def test_get_character_from_swapi_not_found():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"count": 0, "results": []})

    swapi_client = make_swapi_client(handler)

    result = await swapi_client.get_character("unknowncharacter")

    assert result["count"] == 0
    assert len(result["results"]) == 0


async def test_get_character_from_swapi_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"detail": "Internal Server Error"})

    swapi_client = make_swapi_client(handler)

    # HTTP errors are wrapped into the app's own exception at the client boundary
    with pytest.raises(SwapiCharacterError):
        await swapi_client.get_character("vader")


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
