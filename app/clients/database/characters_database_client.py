from sqlalchemy.ext.asyncio import AsyncSession

from app.models.star_wars_character_model import StarWarsCharacter
from app.schemas.swapi_character_schema import SwapiCharacter


async def insert_new_character(
    db: AsyncSession, swapi_character: SwapiCharacter
) -> StarWarsCharacter:
    new_character = StarWarsCharacter(
        name=swapi_character.name,
        height=swapi_character.height,
        mass=swapi_character.mass,
    )
    db.add(new_character)
    # flush assigns the id; the commit happens in get_db_session so one
    # request stays one transaction
    await db.flush()
    return new_character
