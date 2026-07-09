from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.database import characters_database_client
from app.clients.networking.swapi_networking_client import (
    SwapiClient,
    transform_swapi_character_json_to_pydantic,
)
from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.utils.characters_utils import format_star_wars_name


async def add_new_character(
    input_character: StarWarsCharacterCreate,
    db: AsyncSession,
    swapi_client: SwapiClient,
) -> StarWarsCharacterRead:
    swapi_json = await swapi_client.get_character(input_character.name)
    swapi_character = transform_swapi_character_json_to_pydantic(swapi_json)
    swapi_character.name = format_star_wars_name(swapi_character.name)
    new_character = await characters_database_client.insert_new_character(
        db, swapi_character
    )

    return StarWarsCharacterRead.model_validate(new_character)
