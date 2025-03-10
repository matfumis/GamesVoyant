import pytest
from streamlit.runtime.state import SessionState
from modules.auth import *
from modules.database import *
from unittest.mock import patch

MOCK_HASH = "$2b$12$testhashstring"


@pytest.fixture(autouse=True)
def reset_session_state():
    st.session_state.clear()


def test_logout():
    st.session_state.user = "test_user"
    logout()
    assert st.session_state.user is None


def test_get_current_user_user_is_logged():
    st.session_state.user = "test_user"
    assert get_current_user() == "test_user"


def test_get_current_user_user_is_not_logged():
    st.session_state.user = None
    assert get_current_user() is None


@patch("bcrypt.hashpw", return_value=MOCK_HASH.encode())
@patch("modules.auth.get_user", return_value=None)
@patch("modules.auth.add_user")
def test_register_success(mock_add_user, mock_get_user, mock_hashpw):
    st.session_state = SessionState()
    username = "newuser"
    password = "password123"
    name = "John"
    surname = "Doe"
    nationality = "US"
    date_of_birth = "1990-01-01"

    result = register(username, password, name, surname, nationality, date_of_birth)

    assert result is True
    mock_add_user.assert_called_once_with(username, MOCK_HASH, name, surname, nationality,
                                          date_of_birth)


@patch("bcrypt.hashpw", return_value=MOCK_HASH.encode())
@patch("modules.auth.add_user")
@patch("modules.auth.get_user", return_value={"username": "existinguser"})
@patch("streamlit.error")
def test_register_username_exists(mock_st_error, mock_get_user, mock_add_user, mock_hashpw):
    st.session_state = SessionState()
    result = register("existinguser", "password123", "John", "Doe", "US", "1990-01-01")

    assert result is False
    mock_add_user.assert_not_called()
    mock_st_error.assert_called_once_with("Username already exists")


@patch("bcrypt.checkpw", return_value=True)
@patch("modules.auth.get_user", return_value={"username": "testuser", "password_hash": MOCK_HASH})
def test_login_success(mock_get_user, mock_checkpw):
    username = "testuser"
    password = "correct_password"

    result = login(username, password)

    assert result is True
    assert st.session_state.user["username"] == "testuser"


@patch("modules.auth.get_user", return_value=None)
@patch("streamlit.error")
def test_login_user_not_found(mock_st_error, mock_get_user):
    result = login("unknown_user", "any_password")

    assert result is False
    mock_get_user.assert_called_once_with("unknown_user")
    mock_st_error.assert_called_once_with("User not found")


@patch("bcrypt.checkpw", return_value=False)
@patch("modules.auth.get_user", return_value={"username": "testuser", "password_hash": MOCK_HASH})
@patch("streamlit.error")
def test_login_incorrect_password(mock_st_error, mock_get_user, mock_checkpw):
    result = login("testuser", "wrong_password")

    assert result is False
    mock_get_user.assert_called_once_with("testuser")
    mock_checkpw.assert_called_once_with("wrong_password".encode('utf-8'), MOCK_HASH.encode('utf-8'))
    mock_st_error.assert_called_once_with("Incorrect password")
