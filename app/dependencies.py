"""FastAPI dependency wiring.

The routers inject two things: a database session and the SWAPI client.
Services receive both as plain arguments, so this file is the only place
that knows about Depends.
"""

from typing import Annotated

import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.networking.swapi_networking_client import SwapiClient
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
