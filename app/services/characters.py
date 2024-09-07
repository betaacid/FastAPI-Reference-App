from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)


def add_new_character(
    input_character: StarWarsCharacterCreate,
) -> StarWarsCharacterRead:
    new_character = StarWarsCharacterRead(
        id=1,
        name=input_character.name,
        rating=input_character.rating,
        height="123",
        mass="456",
    )
    return new_character
