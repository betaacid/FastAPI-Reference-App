import responses
import requests
from app.clients.networking.swapi_networking_client import get_character_from_swapi

SWAPI_BASE_URL = "https://swapi.dev/api/people/"


@responses.activate
def test_get_character_from_swapi_success(mock_swapi_response):
    search_url = f"{SWAPI_BASE_URL}?search=vader"
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

    search_url = f"{SWAPI_BASE_URL}?search=unknowncharacter"
    responses.add(responses.GET, search_url, json=mock_response_data, status=200)

    result = get_character_from_swapi("unknowncharacter")

    assert result["count"] == 0
    assert len(result["results"]) == 0

    assert responses.calls[0].request.url == search_url
    assert len(responses.calls) == 1


@responses.activate
def test_get_character_from_swapi_error():
    search_url = f"{SWAPI_BASE_URL}?search=vader"
    responses.add(
        responses.GET, search_url, json={"detail": "Internal Server Error"}, status=500
    )

    try:
        get_character_from_swapi("vader")
    except requests.HTTPError:
        pass

    assert responses.calls[0].request.url == search_url
    assert len(responses.calls) == 1
