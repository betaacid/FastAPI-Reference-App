import requests
from typing import Dict

from app.schemas.swapi_character import SwapiCharacter

SWAPI_BASE_URL = "https://swapi.dev/api/people/"


def get_character_from_swapi(name: str) -> Dict:
    url = f"{SWAPI_BASE_URL}?search={name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def transform_swapi_json_to_pydantic(swapi_json: dict) -> SwapiCharacter:
    results = swapi_json.get("results", [])

    if not results:
        raise ValueError("No character found in SWAPI response")

    character_data = results[0]

    return SwapiCharacter(
        name=character_data.get("name"),
        height=character_data.get("height"),
        mass=character_data.get("mass"),
    )
