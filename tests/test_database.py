import pytest
import mysql.connector
import streamlit as st
import json

from modules.database import (
    get_connection,
    get_user,
    add_user,
    search_users,
    add_follow,
    remove_follow,
    add_liked_game,
)

# Dummy classes to simulate a MySQL connection and cursor.
class DummyCursor:
    def __init__(self, user_data=None):
        self.user_data = user_data
        self.closed = False
        self.procname = None
        self.args = None

    def callproc(self, procname, args):
        self.procname = procname
        self.args = args

    def stored_results(self):
        yield self

    def fetchone(self):
        return self.user_data

    def fetchall(self):
        return [self.user_data] if self.user_data else []

    def close(self):
        self.closed = True

class DummyConnection:
    def __init__(self, user_data=None):
        self.user_data = user_data
        self.commit_called = False
        self.closed = False
        self.last_cursor = None

    def is_connected(self):
        return True

    def cursor(self, dictionary=False):
        self.last_cursor = DummyCursor(user_data=self.user_data)
        return self.last_cursor

    def commit(self):
        self.commit_called = True

    def close(self):
        self.closed = True

def dummy_connect_success(*args, **kwargs):
    # Include a user_id in the dummy data for testing.
    return DummyConnection(user_data={"username": "test", "name": "Test", "user_id": 1})

def dummy_connect_failure(*args, **kwargs):
    raise mysql.connector.Error("Connection failed")

# --- Tests ---

def test_get_connection_success(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_success)

    conn = get_connection()
    assert conn is not None
    assert conn.is_connected() is True
    conn.close()

def test_get_connection_failure(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_failure)

    conn = get_connection()
    # On failure, get_connection should return None.
    assert conn is None

def test_get_user(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_success)
    user = get_user("test")
    assert user is not None
    assert user["username"] == "test"

def test_add_user(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    dummy_conn = DummyConnection()

    def dummy_connect_for_add(*args, **kwargs):
        return dummy_conn

    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_for_add)
    add_user("newuser", "hash", "New", "User", "Country", "2000-01-01")
    assert dummy_conn.commit_called is True
    assert dummy_conn.closed is True

def test_add_liked_game(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    dummy_conn = DummyConnection()

    def dummy_connect_for_liked(*args, **kwargs):
        return dummy_conn

    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_for_liked)
    # Call add_liked_game with sample user_id and game_id.
    add_liked_game(1, 100)
    # Verify that the stored procedure was called with the correct name and arguments.
    assert dummy_conn.last_cursor.procname == "AddLikedGame"
    assert dummy_conn.last_cursor.args == [1, 100]
    # Verify that commit was called and connection closed.
    assert dummy_conn.commit_called is True
    assert dummy_conn.closed is True

def test_search_users(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    dummy_user = {"username": "searched", "name": "Searched"}
    dummy_conn = DummyConnection(user_data=dummy_user)

    def dummy_connect_for_search(*args, **kwargs):
        return dummy_conn

    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_for_search)
    results = search_users("searched")
    assert results is not None
    assert isinstance(results, list)
    # Expect the dummy_user to be in the results.
    assert dummy_user in results

def test_add_follow(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    dummy_conn = DummyConnection()

    def dummy_connect_for_follow(*args, **kwargs):
        return dummy_conn

    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_for_follow)
    result = add_follow(1, 2)
    assert result is True
    assert dummy_conn.last_cursor.procname == "AddFollow"
    assert dummy_conn.last_cursor.args == [1, 2]

def test_remove_follow(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb",
        }
    }
    dummy_conn = DummyConnection()

    def dummy_connect_for_remove(*args, **kwargs):
        return dummy_conn

    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_for_remove)
    result = remove_follow(1, 2)
    assert result is True
    assert dummy_conn.last_cursor.procname == "RemoveFollow"
    assert dummy_conn.last_cursor.args == [1, 2]
