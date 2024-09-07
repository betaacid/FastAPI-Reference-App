from app.clients.database.characters_database_client import insert_new_character
from app.clients.networking import swapi_networking_client
from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.models.star_wars_character import StarWarsCharacter
from sqlalchemy.orm import Session


def add_new_character(
    input_character: StarWarsCharacterCreate,
    db: Session,
) -> StarWarsCharacterRead:
    swapi_json = swapi_networking_client.get_character_from_swapi(input_character.name)
    print(swapi_json)
    new_character: StarWarsCharacter = insert_new_character(db, input_character)
    return StarWarsCharacterRead.model_validate(new_character)
