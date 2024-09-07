from app.clients.database.characters_database_client import insert_new_character
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
    new_character: StarWarsCharacter = insert_new_character(db, input_character)
    return StarWarsCharacterRead.model_validate(new_character)
