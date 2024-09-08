from app.clients.database.characters_database_client import insert_new_character


def test_insert_new_character(mock_db_session, mock_swapi_character):
    # When:
    new_character = insert_new_character(mock_db_session, mock_swapi_character)

    # Then:
    assert new_character.name == mock_swapi_character.name


def test_insert_new_character_session_methods_called(
    mock_db_session, mock_swapi_character
):

    # When:
    new_character = insert_new_character(mock_db_session, mock_swapi_character)

    # Then:
    mock_db_session.add.assert_called_once_with(new_character)
    mock_db_session.flush.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(new_character)
    mock_db_session.commit.assert_called_once()