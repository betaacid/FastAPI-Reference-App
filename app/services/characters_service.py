from app.clients.database.characters_database_client import insert_new_character
from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.models.star_wars_character import StarWarsCharacter
from database import get_db_session


def add_new_character(
    input_character: StarWarsCharacterCreate,
) -> StarWarsCharacterRead:
    with get_db_session() as db:
        new_character: StarWarsCharacter = insert_new_character(db, input_character)

        return StarWarsCharacterRead(
            id=new_character.id,
            name=new_character.name,
            rating=new_character.rating,
            height=new_character.height,
            mass=new_character.mass,
        )
