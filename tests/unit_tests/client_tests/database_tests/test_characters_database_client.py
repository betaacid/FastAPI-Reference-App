from app.clients.database.characters_database_client import insert_new_character


async def test_insert_new_character(mock_db_session, mock_swapi_character):
    new_character = await insert_new_character(mock_db_session, mock_swapi_character)

    assert new_character.name == mock_swapi_character.name


async def test_insert_new_character_session_methods_called(
    mock_db_session, mock_swapi_character
):
    new_character = await insert_new_character(mock_db_session, mock_swapi_character)

    mock_db_session.add.assert_called_once_with(new_character)
    mock_db_session.flush.assert_awaited_once()
    # No commit here: the transaction boundary lives in get_db_session
    mock_db_session.commit.assert_not_called()
