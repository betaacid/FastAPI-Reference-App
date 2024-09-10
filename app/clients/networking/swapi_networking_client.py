import requests
from typing import Dict

from app.errors.custom_exceptions import CharacterNotFoundError, SwapiCharacterError
from app.schemas.swapi_character_schema import SwapiCharacter

SWAPI_BASE_URL = "https://swapi.dev/api/people/"


def get_character_from_swapi(name: str) -> Dict:
    url = f"{SWAPI_BASE_URL}?search={name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def transform_swapi_json_to_pydantic(swapi_json: dict) -> SwapiCharacter:
    results = swapi_json.get("results", [])

    if not results:
        raise CharacterNotFoundError("Character not found in SWAPI response")

    try:
        character_data = results[0]
        return SwapiCharacter(
            name=character_data.get("name"),
            height=character_data.get("height"),
            mass=character_data.get("mass"),
        )
    except KeyError as e:
        raise SwapiCharacterError(f"Error parsing SWAPI data: {e}")
