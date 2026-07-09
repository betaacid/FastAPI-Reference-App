"""FastAPI dependency wiring.

All Depends() chains live here so that services and clients stay plain
Python. The nested dependency graph is:

    router -> get_characters_service -> get_characters_db_client -> get_db_session
                                     -> get_swapi_client          -> get_http_client
"""

from typing import Annotated

import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.database.characters_database_client import CharactersDatabaseClient
from app.clients.database.vehicles_database_client import VehiclesDatabaseClient
from app.clients.networking.swapi_networking_client import SwapiClient
from app.services.characters_service import CharactersService
from app.services.vehicles_service import VehiclesService
from database import get_db_session

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_http_client(request: Request) -> httpx.AsyncClient:
    # The shared client is created once at startup in main.py's lifespan
    return request.app.state.http_client


def get_swapi_client(
    http_client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
) -> SwapiClient:
    return SwapiClient(http_client)


SwapiClientDep = Annotated[SwapiClient, Depends(get_swapi_client)]


def get_characters_db_client(db: DbSession) -> CharactersDatabaseClient:
    return CharactersDatabaseClient(db)


def get_characters_service(
    db_client: Annotated[CharactersDatabaseClient, Depends(get_characters_db_client)],
    swapi_client: SwapiClientDep,
) -> CharactersService:
    return CharactersService(db_client, swapi_client)


def get_vehicles_db_client(db: DbSession) -> VehiclesDatabaseClient:
    return VehiclesDatabaseClient(db)


def get_vehicles_service(
    db_client: Annotated[VehiclesDatabaseClient, Depends(get_vehicles_db_client)],
    swapi_client: SwapiClientDep,
) -> VehiclesService:
    return VehiclesService(db_client, swapi_client)
