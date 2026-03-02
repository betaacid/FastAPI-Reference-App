from app.clients.database.characters_database_client import CharactersDatabaseClient


def test_insert_new_character(mock_db_session, mock_swapi_character):
    db_client = CharactersDatabaseClient(db=mock_db_session)

    new_character = db_client.insert_new_character(mock_swapi_character)

    assert new_character.name == mock_swapi_character.name


def test_insert_new_character_session_methods_called(
    mock_db_session, mock_swapi_character
):
    db_client = CharactersDatabaseClient(db=mock_db_session)

    new_character = db_client.insert_new_character(mock_swapi_character)

    mock_db_session.add.assert_called_once_with(new_character)
    mock_db_session.flush.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(new_character)
    mock_db_session.commit.assert_called_once()
