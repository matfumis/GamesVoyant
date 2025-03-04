import mysql.connector
import streamlit as st
from mysql.connector import Error


def get_connection():
    try:
        db_credentials = st.secrets["mysql"]
        connection = mysql.connector.connect(
            host=db_credentials["host"],
            user=db_credentials["user"],
            password=db_credentials["password"],
            database=db_credentials["database"]
        )
        if connection.is_connected():
            print("Connected successfully to database")
        return connection
    except mysql.connector.Error as e:
        st.error(f"Error while connecting: {e}")
        return None


def get_user(username):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('GetUserByUsername', [username])

        user_data = None
        for result in cursor.stored_results():
            user_data = result.fetchone()
        return user_data

    except Error as e:
        print("Error while executing stored procedure:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def get_username(user_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('GetUsername', [user_id])

        user_data = None
        for result in cursor.stored_results():
            user_data = result.fetchone()
        return user_data["username"]

    except Error as e:
        print("Error while executing stored procedure:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def add_user(username, password_hash, name, surname, nationality, date_of_birth):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.callproc("CreateUser", [username, password_hash, name, surname, nationality, date_of_birth])
        conn.commit()
    except Exception as e:
        st.error(f"Error creating user: {e}")
    finally:
        cursor.close()
        conn.close()


def search_users(search_query):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('SearchUsers', [search_query])

        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        return results

    except Error as e:
        print("Error while executing stored procedure:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def add_follow(user_id, other_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.callproc('AddFollow', [user_id, other_id])
        connection.commit()
        return True
    except Error as e:
        print("Error while executing stored procedure AddFollow:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def remove_follow(user_id, other_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.callproc('RemoveFollow', [user_id, other_id])
        connection.commit()
        return True
    except Error as e:
        print("Error while executing stored procedure RemoveFollow:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def add_liked_game(user_id, game_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.callproc("AddLikedGame", [user_id, game_id])
        conn.commit()
    except Exception as e:
        st.error(f"Error updating user's liked games: {e}")
    finally:
        cursor.close()
        conn.close()


def add_disliked_game(user_id, game_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.callproc("AddDislikedGame", [user_id, game_id])
        conn.commit()
    except Exception as e:
        st.error(f"Error updating user's disliked games: {e}")
    finally:
        cursor.close()
        conn.close()


def add_saved_game(user_id, game_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.callproc("AddSavedGame", [user_id, game_id])
        conn.commit()
    except Exception as e:
        st.error(f"Error updating user's saved games: {e}")
    finally:
        cursor.close()
        conn.close()


def remove_liked_game(user_id, game_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.callproc("RemoveLikedGame", [user_id, game_id])
        conn.commit()
    except Exception as e:
        st.error(f"Error updating user's liked games: {e}")
    finally:
        cursor.close()
        conn.close()


def remove_disliked_game(user_id, game_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.callproc("RemoveDislikedGame", [user_id, game_id])
        conn.commit()
    except Exception as e:
        st.error(f"Error updating user's disliked games: {e}")
    finally:
        cursor.close()
        conn.close()


def remove_saved_game(user_id, game_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.callproc("RemoveSavedGame", [user_id, game_id])
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error updating user's saved games: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
