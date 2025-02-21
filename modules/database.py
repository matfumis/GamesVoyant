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
