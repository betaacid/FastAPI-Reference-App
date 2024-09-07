from sqlalchemy.orm import Session
from app.models.star_wars_character import StarWarsCharacter
from app.schemas.star_wars_character import StarWarsCharacterCreate


def insert_new_character(
    db: Session, input_character: StarWarsCharacterCreate
) -> StarWarsCharacter:
    new_character = StarWarsCharacter(
        name=input_character.name,
        rating=input_character.rating,
    )
    db.add(new_character)
    db.flush()

    db.refresh(new_character)
    return new_character
