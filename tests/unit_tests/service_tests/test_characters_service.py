from unittest.mock import AsyncMock, MagicMock, patch

from app.clients.networking.swapi_networking_client import SwapiClient
from app.schemas.star_wars_character_schema import StarWarsCharacterRead
from app.services.characters_service import add_new_character


@patch(
    "app.clients.database.characters_database_client.insert_new_character",
    new_callable=AsyncMock,
)
@patch("app.services.characters_service.transform_swapi_character_json_to_pydantic")
@patch("app.services.characters_service.format_star_wars_name")
async def test_add_new_character_success(
    mock_format_star_wars_name,
    mock_transform_swapi_character_json_to_pydantic,
    mock_insert_new_character,
    mock_db_session,
    mock_star_wars_character_create,
    mock_swapi_character,
    mock_star_wars_character_read,
):
    # MagicMock(spec=...) makes async methods AsyncMocks automatically
    mock_swapi_client = MagicMock(spec=SwapiClient)

    mock_swapi_client.get_character.return_value = {"results": [mock_swapi_character]}
    mock_transform_swapi_character_json_to_pydantic.return_value = mock_swapi_character
    mock_format_star_wars_name.return_value = "Leia_Organa_from_the_starwars_universe"
    mock_insert_new_character.return_value = mock_star_wars_character_read

    result = await add_new_character(
        mock_star_wars_character_create, mock_db_session, mock_swapi_client
    )

    mock_swapi_client.get_character.assert_awaited_once_with("Leia Organa")
    mock_transform_swapi_character_json_to_pydantic.assert_called_once_with(
        {"results": [mock_swapi_character]}
    )
    mock_format_star_wars_name.assert_called_once_with("Leia Organa")
    mock_insert_new_character.assert_awaited_once_with(
        mock_db_session, mock_swapi_character
    )
    assert isinstance(result, StarWarsCharacterRead)
    assert result.name == "Darth Vader"
    assert result.height == "123"
