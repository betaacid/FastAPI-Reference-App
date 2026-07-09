from fastapi import APIRouter

from app.dependencies import DbSession, SwapiClientDep
from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.services import characters_service

characters_router = APIRouter(prefix="/characters")


@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate,
    db: DbSession,
    swapi_client: SwapiClientDep,
) -> StarWarsCharacterRead:
    return await characters_service.add_new_character(input_character, db, swapi_client)
