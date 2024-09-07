import requests
from typing import Dict

SWAPI_BASE_URL = "https://swapi.dev/api/people/"


def get_character_from_swapi(name: str) -> Dict:
    url = f"{SWAPI_BASE_URL}?search={name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
