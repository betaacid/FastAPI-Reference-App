from app.clients.database.characters_database_client import CharactersDatabaseClient
from app.clients.networking.swapi_networking_client import (
    SwapiClient,
    transform_swapi_character_json_to_pydantic,
)
from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.utils.characters_utils import format_star_wars_name


class CharactersService:
    def __init__(self, db_client: CharactersDatabaseClient, swapi_client: SwapiClient):
        self.db_client = db_client
        self.swapi_client = swapi_client

    async def add_new_character(
        self, input_character: StarWarsCharacterCreate
    ) -> StarWarsCharacterRead:
        swapi_json = await self.swapi_client.get_character(input_character.name)
        swapi_character = transform_swapi_character_json_to_pydantic(swapi_json)
        swapi_character.name = format_star_wars_name(swapi_character.name)
        new_character = await self.db_client.insert_new_character(swapi_character)

        return StarWarsCharacterRead.model_validate(new_character)
