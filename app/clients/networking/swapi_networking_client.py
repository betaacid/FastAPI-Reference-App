from typing import Dict

import httpx
from pydantic import ValidationError

from app.errors.custom_exceptions import (
    CharacterNotFoundError,
    SwapiCharacterError,
    SwapiVehicleError,
    VehicleNotFoundError,
)
from app.schemas.swapi_character_schema import SwapiCharacter
from app.schemas.swapi_vehicle_schema import SwapiVehicle

SWAPI_BASE_URL = "https://swapi.dev/api"
SWAPI_TIMEOUT_SECONDS = 10.0


class SwapiClient:
    """Client for the SWAPI API.

    A class because it holds real state: the shared httpx.AsyncClient, which
    owns the connection pool, base URL, and timeout for all SWAPI calls.
    """

    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client

    async def get_character(self, name: str) -> Dict:
        try:
            response = await self.http_client.get("/people/", params={"search": name})
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise SwapiCharacterError(f"Error fetching character from SWAPI: {e}") from e
        return response.json()

    async def get_vehicle(self, name: str) -> Dict:
        try:
            response = await self.http_client.get("/vehicles/", params={"search": name})
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise SwapiVehicleError(f"Error fetching vehicle from SWAPI: {e}") from e
        return response.json()


def transform_swapi_character_json_to_pydantic(swapi_json: dict) -> SwapiCharacter:
    results = swapi_json.get("results", [])

    if not results:
        raise CharacterNotFoundError("Character not found in SWAPI response")

    character_data = results[0]
    try:
        return SwapiCharacter(
            name=character_data.get("name"),
            height=character_data.get("height"),
            mass=character_data.get("mass"),
        )
    except ValidationError as e:
        raise SwapiCharacterError(f"Error parsing SWAPI data: {e}") from e


def transform_swapi_vehicle_json_to_pydantic(swapi_json: dict) -> SwapiVehicle:
    results = swapi_json.get("results", [])

    if not results:
        raise VehicleNotFoundError("Vehicle not found in SWAPI response")

    vehicle_data = results[0]
    try:
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
    except ValidationError as e:
        raise SwapiVehicleError(f"Error parsing SWAPI data: {e}") from e
