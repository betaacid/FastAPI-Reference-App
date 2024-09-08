from app.clients.database.characters_database_client import insert_new_character
from app.clients.networking.swapi_networking_client import (
    get_character_from_swapi,
    transform_swapi_json_to_pydantic,
)
from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.models.star_wars_character import StarWarsCharacter
from sqlalchemy.orm import Session

from app.utils.characters_utils import format_star_wars_name


def add_new_character(
    input_character: StarWarsCharacterCreate,
    db: Session,
) -> StarWarsCharacterRead:
    swapi_json = get_character_from_swapi(input_character.name)
    try:
        swapi_character = transform_swapi_json_to_pydantic(swapi_json)
        formatted_name = format_star_wars_name(swapi_character.name)
        swapi_character.name = formatted_name
        new_character: StarWarsCharacter = insert_new_character(db, swapi_character)
        return StarWarsCharacterRead.model_validate(new_character)
    except ValueError as e:
        raise ValueError(f"Error while fetching character from SWAPI: {e}")
