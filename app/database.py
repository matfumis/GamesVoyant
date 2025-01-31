import mysql.connector
import streamlit as st

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
            print("Connected sucesfully to database")
        return connection
    except Error as e:
        print(f"Error while connecting: {e}")
        return None

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def create_user(username, password_hash, name, surname, nationality, date_of_birth):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("CreateUser", [username, password_hash, name, surname, nationality, date_of_birth])
    conn.commit()
    cursor.close()
    conn.close()
