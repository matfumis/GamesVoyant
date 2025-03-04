import json
import bcrypt
import pytest
import streamlit as st

from modules.auth import register, login, logout, get_current_user


def fake_get_user_none(username):
    return None


def fake_get_user_existing(username):
    password = "secret"
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return {
        "username": username,
        "password_hash": hashed,
        "name": "Test",
        "surname": "User",
        "nationality": "TestLand",
        "date_of_birth": "2000-01-01",
        "saved_games": "[]",
        "followed_users": "[]",
        "user_id": 1,
    }


def fake_add_user(username, password_hash, name, surname, nationality, date_of_birth):
    return


class ErrorCapture:
    def __init__(self):
        self.errors = []

    def __call__(self, message):
        self.errors.append(message)


# --- Tests ---

@pytest.fixture(autouse=True)
def reset_session_state():
    if "user" in st.session_state:
        del st.session_state["user"]
    yield
    if "user" in st.session_state:
        del st.session_state["user"]


def test_register_success(monkeypatch):
    monkeypatch.setattr("modules.auth.get_user", fake_get_user_none)
    monkeypatch.setattr("modules.auth.add_user", fake_add_user)

    error_capture = ErrorCapture()
    monkeypatch.setattr(st, "error", error_capture)

    result = register("newuser", "password123", "Alice", "Smith", "Wonderland", "1990-01-01")
    assert result is True
    assert error_capture.errors == []


def test_register_existing(monkeypatch):
    monkeypatch.setattr("modules.auth.get_user", fake_get_user_existing)
    error_capture = ErrorCapture()
    monkeypatch.setattr(st, "error", error_capture)

    result = register("existinguser", "password123", "Bob", "Jones", "Nowhere", "1990-01-01")
    assert result is False
    assert any("Username already exists" in err for err in error_capture.errors)


def test_register_exception(monkeypatch):
    monkeypatch.setattr("modules.auth.get_user", fake_get_user_none)

    def fake_add_user_error(*args, **kwargs):
        raise Exception("DB error")

    monkeypatch.setattr("modules.auth.add_user", fake_add_user_error)
    error_capture = ErrorCapture()
    monkeypatch.setattr(st, "error", error_capture)

    result = register("erroruser", "password123", "Carol", "Doe", "Testland", "1990-01-01")
    assert result is False
    assert any("Error during registration" in err for err in error_capture.errors)


def test_login_success(monkeypatch):
    monkeypatch.setattr("modules.auth.get_user", fake_get_user_existing)
    error_capture = ErrorCapture()
    monkeypatch.setattr(st, "error", error_capture)

    result = login("testuser", "secret")
    assert result is True
    current = get_current_user()
    assert current is not None
    assert current["username"] == "testuser"
    assert error_capture.errors == []


def test_login_user_not_found(monkeypatch):
    monkeypatch.setattr("modules.auth.get_user", fake_get_user_none)
    error_capture = ErrorCapture()
    monkeypatch.setattr(st, "error", error_capture)

    result = login("nonexistent", "any_password")
    assert result is False
    assert any("User not found" in err for err in error_capture.errors)


def test_login_incorrect_password(monkeypatch):
    monkeypatch.setattr("modules.auth.get_user", fake_get_user_existing)
    error_capture = ErrorCapture()
    monkeypatch.setattr(st, "error", error_capture)

    result = login("testuser", "wrongpassword")
    assert result is False
    assert any("Incorrect password" in err for err in error_capture.errors)


def test_logout(monkeypatch):
    st.session_state.user = {"username": "testuser"}
    logout()
    assert st.session_state.get("user") is None


def test_get_current_user(monkeypatch):
    st.session_state.user = {"username": "testuser"}
    user = get_current_user()
    assert user["username"] == "testuser"
