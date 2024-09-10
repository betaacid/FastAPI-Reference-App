from unittest.mock import patch
import pytest
from fastapi import HTTPException
from app.errors.custom_exceptions import CharacterNotFoundError
from app.services.characters_service import add_new_character
from app.schemas.star_wars_character_schema import StarWarsCharacterRead
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError


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
    mock_insert_new_character.side_effect = SQLAlchemyError("Database insertion error")

    # When / Then: Expect an HTTPException (500 Internal Server Error) to be raised
    with pytest.raises(HTTPException) as exc_info:
        add_new_character(mock_star_wars_character_create, mock_db_session)

    assert exc_info.value.status_code == 500
    mock_transform_swapi_json_to_pydantic.assert_called_once_with(
        {"results": [mock_swapi_character]}
    )
    mock_insert_new_character.assert_called_once_with(
        mock_db_session, mock_swapi_character
    )


@patch("app.services.characters_service.get_character_from_swapi")
@patch("app.services.characters_service.transform_swapi_json_to_pydantic")
def test_add_new_character_networking_error(
    mock_transform_swapi_json_to_pydantic,
    mock_get_character_from_swapi,
    mock_db_session,
    mock_star_wars_character_create,
):
    # Simulate a networking error (e.g., SWAPI is down)
    mock_get_character_from_swapi.side_effect = RequestException("Network error")

    # When / Then: Expect an HTTPException (503 Service Unavailable) to be raised
    with pytest.raises(HTTPException) as exc_info:
        add_new_character(mock_star_wars_character_create, mock_db_session)

    assert exc_info.value.status_code == 503
