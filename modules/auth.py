import streamlit as st
import bcrypt
from modules import database  # This module provides get_user and add_user


def register(username, password, name, surname, nationality, date_of_birth):
    if database.get_user(username) is not None:
        st.error("Username già esistente")
        return False

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        database.add_user(username, password_hash, name, surname, nationality, date_of_birth)
        st.success("Registrazione avvenuta con successo!")
        return True
    except Exception as e:
        st.error(f"Errore durante la registrazione: {e}")
        return False


def login(username, password):
    user = database.get_user(username)
    if user is None:
        st.error("Utente non trovato")
        return False

    stored_hash = user["password_hash"].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        st.session_state.user = user
        st.success("Login effettuato con successo!")
        return True
    else:
        st.error("Password errata")
        return False


def logout():
    st.session_state.user = None


def get_current_user():
    return st.session_state.get("user", None)
