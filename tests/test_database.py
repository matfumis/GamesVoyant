import pytest
import mysql.connector
import streamlit as st

from modules.database import *

class DummyCursor:
    def __init__(self, user_data=None):
        self.user_data = user_data
        self.closed = False

    def callproc(self, procname, args):
        self.procname = procname
        self.args = args

    def stored_results(self):
        yield self

    def fetchone(self):
        return self.user_data

    def close(self):
        self.closed = True

class DummyConnection:
    def __init__(self, user_data=None):
        self.user_data = user_data
        self.commit_called = False
        self.closed = False

    def is_connected(self):
        return True

    def cursor(self, dictionary=False):
        return DummyCursor(user_data=self.user_data)

    def commit(self):
        self.commit_called = True

    def close(self):
        self.closed = True


def dummy_connect_success(*args, **kwargs):
    return DummyConnection(user_data={"username": "test", "name": "Test"})

def dummy_connect_failure(*args, **kwargs):
    raise mysql.connector.Error("Connection failed")

# --- Tests ---

def test_get_connection_success(monkeypatch):
    st.secrets = {
        "mysql": {
            "host": "localhost",
            "user": "test",
            "password": "test",
            "database": "testdb"
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
            "database": "testdb"
        }
    }
    # Force a failure by monkeypatching to our dummy_connect_failure.
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
            "database": "testdb"
        }
    }
    # For get_user, simulate a successful connection returning dummy user data.
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
            "database": "testdb"
        }
    }
    dummy_conn = DummyConnection()
    def dummy_connect_for_add(*args, **kwargs):
        return dummy_conn

    monkeypatch.setattr(mysql.connector, "connect", dummy_connect_for_add)
    add_user("newuser", "hash", "New", "User", "Country", "2000-01-01")
    assert dummy_conn.commit_called is True
    assert dummy_conn.closed is True
