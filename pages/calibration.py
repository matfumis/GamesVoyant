import json
import streamlit as st
import pandas as pd
import numpy as np
from modules.auth import get_current_user
from modules.database import add_liked_game 

games_path = "data/clusteredDataset.pkl"

user = get_current_user()
if user is None:
    st.switch_page("app.py")
    st.stop()

st.set_page_config(layout="wide")
st.title("Choose your favorite games")

games_liked_raw = user.get("games_liked", "[]")
try:
    games_liked = json.loads(games_liked_raw) if isinstance(games_liked_raw, str) else list(games_liked_raw)
    games_liked = [int(x) for x in games_liked]
except Exception:
    games_liked = []

df = pd.read_pickle(games_path)

df["Cluster_fake"] = np.random.randint(0, 21, size=len(df))

sorted_df = df.sort_values(by="Positive", ascending=False)

grid_df = sorted_df.head(20)

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
                        <p>Positive: {game["Positive"]}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.write("No image available")
            
            app_id = int(game["AppID"])
            default_value = app_id in games_liked
            selected = st.checkbox("Select", value=default_value, key=f"game_{app_id}")
            selected_games[app_id] = selected

updated_games_liked = [app_id for app_id, selected in selected_games.items() if selected]

st.write("Liked games:", updated_games_liked)

if st.button("Submit"):
    if not (1 <= len(updated_games_liked) <= 3):
        st.error("Please select between 1 and 3 games")
    else:
        for game_id in updated_games_liked:
            add_liked_game(get_current_user()['user_id'], game_id)
        st.success("Preferences updated successfully.")
        st.switch_page("pages/home.py")
