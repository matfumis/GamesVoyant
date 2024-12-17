import streamlit as st
from utils.database import create_connection, get_games_by_genre, search_user

st.title("GamesVoyant 🔮👾")
connection = create_connection()

st.sidebar.title("Menu")
menu = st.sidebar.selectbox("Select", ["Home", "Search Games", "Search Users"])


if menu == "Home":
  st.write("Welcome ")

elif menu == "Search Games":
  genre = st.text_input("Insert game name")
  if st.button("Search"):
    games = get_games_by_genre(connection, genre)
    for game in games:
      st.write(f"Title: {game[1]}, Ganre: {game[2]}")

elif menu == "Search Users":
  username = st.text_input("Insert username or part of it")
  if st.button("Search"):
    users = search_user(connection, username)
    for user in users:
      st.write(f"ID: {user[0]}")
      st.write(f"Username: {user[1]}")
      st.write(f"Name: {user[2]}")
      st.write(f"Surname: {user[3]}")
      st.write(f"Nationality: {user[4]}")
      st.write(f"Birthday: {user[5]}")
      st.write("---")