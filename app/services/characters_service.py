from app.clients.database.characters_database_client import insert_new_character
from app.clients.networking.swapi_networking_client import (
    get_character_from_swapi,
    transform_swapi_json_to_pydantic,
)
from app.errors.custom_exceptions import CharacterNotFoundError, SwapiCharacterError
from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.models.star_wars_character_model import StarWarsCharacter
from sqlalchemy.orm import Session
from fastapi import HTTPException
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.utils.characters_utils import format_star_wars_name


def add_new_character(
    input_character: StarWarsCharacterCreate,
    db: Session,
) -> StarWarsCharacterRead:
    swapi_json = get_character_from_swapi(input_character.name)
    swapi_character = transform_swapi_json_to_pydantic(swapi_json)
    swapi_character.name = format_star_wars_name(swapi_character.name)

    try:
        new_character: StarWarsCharacter = insert_new_character(db, swapi_character)

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return StarWarsCharacterRead.model_validate(new_character)
