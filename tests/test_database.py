import pytest
from unittest.mock import patch, MagicMock
import mysql.connector
from mysql.connector import Error
import streamlit as st
import modules.database as db

@pytest.fixture(autouse=True)
def mock_st_secrets():
    with patch.object(st, 'secrets', {'mysql': {
        'host': 'test_host',
        'user': 'test_user',
        'password': 'test_password',
        'database': 'test_db'
    }}):
        yield

@pytest.fixture
def mock_connection():
    mock_conn = MagicMock()
    mock_conn.is_connected.return_value = True
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch('mysql.connector.connect', return_value=mock_conn):
        yield mock_conn, mock_cursor

def test_get_connection(mock_connection):
    mock_conn, _ = mock_connection
    connection = db.get_connection()
    assert connection is mock_conn

def test_get_user(mock_connection):
    _, mock_cursor = mock_connection

    mock_result = MagicMock()
    mock_result.fetchone.return_value = {'id': 1, 'username': 'testuser', 'name': 'Test User'}
    mock_cursor.stored_results.return_value = [mock_result]

    result = db.get_user('testuser')

    mock_cursor.callproc.assert_called_with('GetUserByUsername', ['testuser'])

    assert result == {'id': 1, 'username': 'testuser', 'name': 'Test User'}

def test_get_username(mock_connection):
    _, mock_cursor = mock_connection

    mock_result = MagicMock()
    mock_result.fetchone.return_value = {'username': 'testuser'}
    mock_cursor.stored_results.return_value = [mock_result]

    result = db.get_username(1)

    mock_cursor.callproc.assert_called_with('GetUsername', [1])
    assert result == 'testuser'

def test_add_user(mock_connection):
    _, mock_cursor = mock_connection

    db.add_user('testuser', 'hash123', 'Test', 'User', 'US', '2000-01-01')

    mock_cursor.callproc.assert_called_with('CreateUser',
                                            ['testuser', 'hash123', 'Test', 'User', 'US', '2000-01-01'])

def test_search_users(mock_connection):
    _, mock_cursor = mock_connection

    mock_result = MagicMock()
    mock_result.fetchall.return_value = [
        {'id': 1, 'username': 'testuser1'},
        {'id': 2, 'username': 'testuser2'}
    ]
    mock_cursor.stored_results.return_value = [mock_result]

    results = db.search_users('test')

    mock_cursor.callproc.assert_called_with('SearchUsers', ['test'])
    assert len(results) == 2
    assert results[0]['username'] == 'testuser1'
    assert results[1]['username'] == 'testuser2'

def test_add_follow(mock_connection):
    _, mock_cursor = mock_connection

    result = db.add_follow(1, 2)

    mock_cursor.callproc.assert_called_with('AddFollow', [1, 2])
    assert result is True

def test_get_user_error(mock_connection):
    _, mock_cursor = mock_connection

    mock_cursor.callproc.side_effect = Error("Database error")

    result = db.get_user('testuser')
    assert result is None

def test_remove_follow(mock_connection):
    _, mock_cursor = mock_connection

    result = db.remove_follow(1, 2)

    mock_cursor.callproc.assert_called_with('RemoveFollow', [1, 2])
    assert result is True

def test_add_liked_game(mock_connection):
    _, mock_cursor = mock_connection

    db.add_liked_game(1, 100)

    mock_cursor.callproc.assert_called_with('AddLikedGame', [1, 100])

def test_add_disliked_game(mock_connection):
    _, mock_cursor = mock_connection

    db.add_disliked_game(1, 100)

    mock_cursor.callproc.assert_called_with('AddDislikedGame', [1, 100])

def test_add_saved_game(mock_connection):
    _, mock_cursor = mock_connection

    db.add_saved_game(1, 100)

    mock_cursor.callproc.assert_called_with('AddSavedGame', [1, 100])

def test_remove_liked_game(mock_connection):
    _, mock_cursor = mock_connection

    db.remove_liked_game(1, 100)

    mock_cursor.callproc.assert_called_with('RemoveLikedGame', [1, 100])

def test_remove_disliked_game(mock_connection):
    _, mock_cursor = mock_connection

    db.remove_disliked_game(1, 100)

    mock_cursor.callproc.assert_called_with('RemoveDislikedGame', [1, 100])

def test_remove_saved_game(mock_connection):
    _, mock_cursor = mock_connection

    result = db.remove_saved_game(1, 100)

    mock_cursor.callproc.assert_called_with('RemoveSavedGame', [1, 100])
    assert result is True


def test_remove_saved_game_error(mock_connection):
    _, mock_cursor = mock_connection

    mock_cursor.callproc.side_effect = Exception("Database error")

    with patch('streamlit.error') as mock_error:
        result = db.remove_saved_game(1, 100)
        assert result is False
        mock_error.assert_called_once()

def test_get_connection_error():
    with patch('mysql.connector.connect', side_effect=mysql.connector.Error("Connection error")):
        with patch('streamlit.error') as mock_st_error:
            connection = db.get_connection()
            assert connection is None
            mock_st_error.assert_called_once()

def test_add_user_exception():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.callproc.side_effect = Exception("Test error")
    
    with patch('modules.database.get_connection', return_value=mock_conn):
        with patch('streamlit.error') as mock_st_error:
            db.add_user('testuser', 'hash123', 'Test', 'User', 'US', '2000-01-01')
            mock_st_error.assert_called_once()