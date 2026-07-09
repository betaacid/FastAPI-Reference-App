from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, status

from app.clients.networking.swapi_networking_client import (
    SWAPI_BASE_URL,
    SWAPI_TIMEOUT_SECONDS,
)
from app.errors.custom_exceptions import (
    CharacterNotFoundError,
    SwapiCharacterError,
    SwapiVehicleError,
    VehicleNotFoundError,
)
from app.errors.exception_handlers import (
    character_not_found_error_handler,
    index_out_of_range_error_handler,
    not_found_error_handler,
    server_error_handler,
    swapi_character_error_handler,
    swapi_vehicle_error_handler,
    vehicle_not_found_error_handler,
)
from app.routers.characters_router import characters_router
from app.routers.vehicles_router import vehicles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # One shared HTTP client for the app's lifetime: connection pooling,
    # base URL, and timeout configured in a single place.
    app.state.http_client = httpx.AsyncClient(
        base_url=SWAPI_BASE_URL, timeout=SWAPI_TIMEOUT_SECONDS
    )
    yield
    await app.state.http_client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(characters_router)
app.include_router(vehicles_router)

app.add_exception_handler(SwapiCharacterError, swapi_character_error_handler)
app.add_exception_handler(SwapiVehicleError, swapi_vehicle_error_handler)
app.add_exception_handler(CharacterNotFoundError, character_not_found_error_handler)
app.add_exception_handler(VehicleNotFoundError, vehicle_not_found_error_handler)
app.add_exception_handler(IndexError, index_out_of_range_error_handler)
app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_error_handler)
app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, server_error_handler)
