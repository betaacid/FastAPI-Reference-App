from sqlalchemy.ext.asyncio import AsyncSession

from app.models.star_wars_character_model import StarWarsCharacter
from app.schemas.swapi_character_schema import SwapiCharacter


class CharactersDatabaseClient:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def insert_new_character(
        self, swapi_character: SwapiCharacter
    ) -> StarWarsCharacter:
        new_character = StarWarsCharacter(
            name=swapi_character.name,
            height=swapi_character.height,
            mass=swapi_character.mass,
        )
        self.db.add(new_character)
        # flush assigns the id; the commit happens in get_db_session so one
        # request stays one transaction
        await self.db.flush()
        return new_character
