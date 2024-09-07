from app.clients.database.characters_database_client import insert_new_character
from app.schemas.star_wars_character import StarWarsCharacterCreate


def test_insert_new_character(mock_db_session, mock_star_wars_character_create):
    # When:
    new_character = insert_new_character(
        mock_db_session, mock_star_wars_character_create
    )

    # Then:
    assert new_character.name == mock_star_wars_character_create.name
    assert new_character.rating == mock_star_wars_character_create.rating


def test_insert_new_character_session_methods_called(
    mock_db_session, mock_star_wars_character_create
):

    # When:
    new_character = insert_new_character(
        mock_db_session, mock_star_wars_character_create
    )

    # Then:
    mock_db_session.add.assert_called_once_with(new_character)
    mock_db_session.flush.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(new_character)
    mock_db_session.commit.assert_called_once()
