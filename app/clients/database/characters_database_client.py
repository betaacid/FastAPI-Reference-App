from sqlalchemy.orm import Session
from app.models.star_wars_character import StarWarsCharacter
from app.schemas.star_wars_character import StarWarsCharacterCreate
from app.schemas.swapi_character import SwapiCharacter


def insert_new_character(
    db: Session, swapi_character: SwapiCharacter
) -> StarWarsCharacter:
    new_character = StarWarsCharacter(
        name=swapi_character.name,
        height=swapi_character.height,
        mass=swapi_character.mass,
    )
    db.add(new_character)
    db.flush()
    db.refresh(new_character)
    db.commit()
    return new_character
