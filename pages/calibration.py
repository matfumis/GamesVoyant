import json
import streamlit as st
import pandas as pd
import numpy as np
from modules.auth import get_current_user
from modules.database import *

games_path = "data/clusteredDataset.pkl"

user = get_current_user()
if user is None:
    st.switch_page("app.py")
    st.stop()

user = get_user_by_id(user["user_id"])

st.set_page_config(layout="wide")
st.title("Choose your favorite games")

games_liked_raw = user.get("games_liked", "[]")
try:
    games_liked = json.loads(games_liked_raw) if isinstance(games_liked_raw, str) else list(games_liked_raw)
    games_liked = [int(x) for x in games_liked]
except Exception:
    games_liked = []

df = pd.read_pickle(games_path)

top_1000 = df.sort_values(by="Positive", ascending=False).head(1000)

n_of_games = 40

if "grid_df" not in st.session_state:
    st.session_state.grid_df = top_1000.sample(n_of_games)

grid_df = st.session_state.grid_df

num_columns = 5
selected_games = {}

for i in range(0, len(grid_df), num_columns):
    cols = st.columns(num_columns)
    for col, (_, game) in zip(cols, grid_df.iloc[i:i+num_columns].iterrows()):
        with col:
            if 'Header image' in game and pd.notnull(game['Header image']):
                img = game.get("Header image")
                st.image(img, use_column_width=True)
                col.markdown(f"""
                    <div style="height:120px; overflow-y:auto">
                        <h4 style="margin-bottom: 0.25rem;">{game["Name"]}</h4>
                        <p style="color: gray; margin-top: 0rem;">Release: {game["Release date"]}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.write("No image available")
            
            app_id = int(game["AppID"])
            default_value = app_id in games_liked
            selected = st.checkbox("Select", value=default_value, key=f"game_{app_id}")
            selected_games[app_id] = selected

updated_games_liked = [app_id for app_id, selected in selected_games.items() if selected]

if st.button("Submit"):
    if not (5 <= len(updated_games_liked)):
        st.error("Please select at least 5 games")
    else:
        for game_id in updated_games_liked:
            add_liked_game(get_current_user()['user_id'], game_id)
        st.success("Preferences updated successfully.")
        st.switch_page("pages/home.py")
