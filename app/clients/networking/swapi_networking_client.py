import requests
from typing import Dict

from app.errors.custom_exceptions import (
    CharacterNotFoundError,
    SwapiCharacterError,
    SwapiVehicleError,
    VehicleNotFoundError,
)
from app.schemas.swapi_character_schema import SwapiCharacter
from app.schemas.swapi_vehicle_schema import SwapiVehicle

SWAPI_BASE_URL = "https://swapi.dev/api"


def get_character_from_swapi(name: str) -> Dict:
    url = f"{SWAPI_BASE_URL}/people/?search={name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_vehicle_from_swapi(name: str) -> Dict:
    url = f"{SWAPI_BASE_URL}/vehicles/?search={name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def transform_swapi_character_json_to_pydantic(swapi_json: dict) -> SwapiCharacter:
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


def transform_swapi_vehicle_json_to_pydantic(swapi_json: dict) -> SwapiVehicle:
    results = swapi_json.get("results", [])

    if not results:
        raise VehicleNotFoundError("Vehicle not found in SWAPI response")

    try:
        vehicle_data = results[0]
        return SwapiVehicle(
            name=vehicle_data.get("name"),
            model=vehicle_data.get("model"),
            manufacturer=vehicle_data.get("manufacturer"),
            cost_in_credits=vehicle_data.get("cost_in_credits"),
            length=vehicle_data.get("length"),
            max_atmosphering_speed=vehicle_data.get("max_atmosphering_speed"),
            crew=vehicle_data.get("crew"),
            passengers=vehicle_data.get("passengers"),
            cargo_capacity=vehicle_data.get("cargo_capacity"),
            consumables=vehicle_data.get("consumables"),
            vehicle_class=vehicle_data.get("vehicle_class"),
        )

    except KeyError as e:
        raise SwapiVehicleError(f"Error parsing SWAPI data: {e}")
