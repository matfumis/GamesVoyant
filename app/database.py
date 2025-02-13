import mysql.connector
import streamlit as st
import pandas as pd

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

def load_random_games(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM games_data ORDER BY RAND() LIMIT 10;")
    games = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(games)

import json
import streamlit as st
import mysql.connector

def update_user_games_liked(user_id, games_liked):
    conn = get_connection()  
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        query = "UPDATE Users SET games_liked = %s WHERE user_id = %s"
        

        games_liked_json = json.dumps(games_liked)
        
        cursor.execute(query, (games_liked_json, user_id))
        conn.commit()
    except Exception as e:
        st.error(f"Error updating user's liked games: {e}")
    finally:
        cursor.close()
        conn.close()
