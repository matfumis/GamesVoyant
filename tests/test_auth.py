import pytest
import bcrypt
import streamlit as st
from modules.auth import *


@pytest.fixture(autouse=True)
def clear_session_state():
    st.session_state.clear()
    yield
    st.session_state.clear()


@pytest.fixture
def capture_messages(monkeypatch):
    messages = {"error": [], "success": []}
    monkeypatch.setattr(st, "error", lambda msg: messages["error"].append(msg))
    monkeypatch.setattr(st, "success", lambda msg: messages["success"].append(msg))
    return messages


def test_register_user_exists(monkeypatch, capture_messages):
    monkeypatch.setattr("modules.database.get_user", lambda username: {"username": username})

    result = register("existing_user", "password", "Name", "Surname", "Nationality", "2000-01-01")
    assert result is False
    assert any("Username already exists" in msg for msg in capture_messages["error"])


def test_register_success(monkeypatch, capture_messages):
    monkeypatch.setattr("modules.database.get_user", lambda username: None)

    add_user_called = False

    def dummy_add_user(username, password_hash, name, surname, nationality, date_of_birth):
        nonlocal add_user_called
        add_user_called = True

    monkeypatch.setattr("modules.database.add_user", dummy_add_user)

    result = register("new_user", "mypassword", "Name", "Surname", "Nationality", "2000-01-01")
    assert result is True
    assert add_user_called is True


def test_register_exception(monkeypatch, capture_messages):
    monkeypatch.setattr("modules.database.get_user", lambda username: None)

    def dummy_add_user(username, password_hash, name, surname, nationality, date_of_birth):
        raise Exception("DB error")

    monkeypatch.setattr("modules.database.add_user", dummy_add_user)

    result = register("new_user", "mypassword", "Name", "Surname", "Nationality", "2000-01-01")
    assert result is False
    assert any("Error during registration" in msg for msg in capture_messages["error"])


def test_login_user_not_found(monkeypatch, capture_messages):
    monkeypatch.setattr("modules.database.get_user", lambda username: None)

    result = login("nonexistent", "password")
    assert result is False
    assert any("User not found" in msg for msg in capture_messages["error"])


def test_login_success(monkeypatch, capture_messages):
    password = "secret"
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {"username": "test", "password_hash": password_hash, "name": "Test"}

    monkeypatch.setattr("modules.database.get_user", lambda username: user_data)

    result = login("test", password)
    assert result is True
    assert st.session_state.get("user") == user_data


def test_login_incorrect_password(monkeypatch, capture_messages):
    correct_password = "correct"
    wrong_password = "wrong"
    password_hash = bcrypt.hashpw(correct_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {"username": "test", "password_hash": password_hash, "name": "Test"}

    monkeypatch.setattr("modules.database.get_user", lambda username: user_data)

    result = login("test", wrong_password)
    assert result is False
    assert st.session_state.get("user") is None
    assert any("Incorrect password" in msg for msg in capture_messages["error"])


def test_logout_and_get_current_user():
    st.session_state.user = {"username": "test", "name": "Test"}
    user = get_current_user()
    assert user is not None
    assert user["username"] == "test"

    logout()
    user_after_logout = get_current_user()
    assert user_after_logout is None
