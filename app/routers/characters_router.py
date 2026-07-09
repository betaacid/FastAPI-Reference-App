from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_characters_service
from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.services.characters_service import CharactersService

characters_router = APIRouter(prefix="/characters")


@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate,
    service: Annotated[CharactersService, Depends(get_characters_service)],
) -> StarWarsCharacterRead:
    return await service.add_new_character(input_character)
