from unittest.mock import patch
import pytest
from app.services.characters_service import add_new_character
from app.schemas.star_wars_character import StarWarsCharacterRead


@patch("app.services.characters_service.get_character_from_swapi")
@patch("app.services.characters_service.transform_swapi_json_to_pydantic")
@patch("app.services.characters_service.insert_new_character")
@patch("app.services.characters_service.format_star_wars_name")
def test_add_new_character_success(
    mock_format_star_wars_name,
    mock_insert_new_character,
    mock_transform_swapi_json_to_pydantic,
    mock_get_character_from_swapi,
    mock_db_session,
    mock_star_wars_character_create,
    mock_swapi_character,
    mock_star_wars_character_read,
):
    # Given
    mock_get_character_from_swapi.return_value = {"results": [mock_swapi_character]}
    mock_transform_swapi_json_to_pydantic.return_value = mock_swapi_character
    mock_format_star_wars_name.return_value = "Leia_Organa_from_the_starwars_universe"
    mock_insert_new_character.return_value = mock_star_wars_character_read

    # When
    result = add_new_character(mock_star_wars_character_create, mock_db_session)

    # Then
    mock_get_character_from_swapi.assert_called_once_with("Leia Organa")
    mock_transform_swapi_json_to_pydantic.assert_called_once_with(
        {"results": [mock_swapi_character]}
    )
    mock_format_star_wars_name.assert_called_once_with("Leia Organa")
    mock_insert_new_character.assert_called_once_with(
        mock_db_session, mock_swapi_character
    )
    assert isinstance(result, StarWarsCharacterRead)
    assert result.name == "Darth Vader"
    assert result.height == "123"


@patch("app.services.characters_service.get_character_from_swapi")
@patch("app.services.characters_service.transform_swapi_json_to_pydantic")
def test_add_new_character_swapi_error(
    mock_transform_swapi_json_to_pydantic,
    mock_get_character_from_swapi,
    mock_db_session,
    mock_star_wars_character_create,
):
    # Given: SWAPI call returns no character (empty results)
    mock_get_character_from_swapi.return_value = {"results": []}
    mock_transform_swapi_json_to_pydantic.side_effect = ValueError(
        "Character not found in SWAPI"
    )

    # When / Then: Expect a ValueError when the character is not found
    with pytest.raises(
        ValueError,
        match="Error while fetching character from SWAPI: Character not found in SWAPI",
    ):
        add_new_character(mock_star_wars_character_create, mock_db_session)

    mock_get_character_from_swapi.assert_called_once_with("Leia Organa")
    mock_transform_swapi_json_to_pydantic.assert_called_once_with({"results": []})


@patch("app.services.characters_service.get_character_from_swapi")
@patch("app.services.characters_service.transform_swapi_json_to_pydantic")
@patch("app.services.characters_service.insert_new_character")
def test_add_new_character_db_insert_error(
    mock_insert_new_character,
    mock_transform_swapi_json_to_pydantic,
    mock_get_character_from_swapi,
    mock_db_session,
    mock_star_wars_character_create,
    mock_swapi_character,
):
    # Given: Simulate a successful SWAPI response
    mock_get_character_from_swapi.return_value = {"results": [mock_swapi_character]}
    mock_transform_swapi_json_to_pydantic.return_value = mock_swapi_character

    # Simulate a database insertion error
    mock_insert_new_character.side_effect = Exception("Database insertion error")

    # When / Then: Expect an exception to be raised
    with pytest.raises(Exception, match="Database insertion error"):
        add_new_character(mock_star_wars_character_create, mock_db_session)

    mock_get_character_from_swapi.assert_called_once_with("Leia Organa")
    mock_transform_swapi_json_to_pydantic.assert_called_once_with(
        {"results": [mock_swapi_character]}
    )
    mock_insert_new_character.assert_called_once_with(
        mock_db_session, mock_swapi_character
    )
