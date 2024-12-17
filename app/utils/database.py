import mysql.connector
from mysql.connector import Error
import streamlit as st


def create_connection():
    try:
        db_credentials = st.secrets["mysql"]

        connection = mysql.connector.connect(
            host=db_credentials["host"],
            user=db_credentials["user"],
            password=db_credentials["password"],
            database=db_credentials["database"]

        )
        if connection.is_connected():
            print("Connesso al database")
        return connection
    except Error as e:
        print(f"Errore di connessione: {e}")
        return None


def get_games_by_genre(connection, genre):
    try:
        cursor = connection.cursor()
        # Chiamare la stored procedure
        cursor.callproc('GetGamesByGenre', [genre])

        # Recuperare i risultati
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())

        return results
    except Error as e:
        print(f"Errore durante l'esecuzione della stored procedure: {e}")
        return []

def search_user(connection, username):
    try:
        cursor = connection.cursor()
        # Chiamare la stored procedure
        cursor.callproc('SearchUser', [username])

        # Recuperare i risultati
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())

        return results
    except Error as e:
        print(f"Errore durante l'esecuzione della stored procedure: {e}")
        return []