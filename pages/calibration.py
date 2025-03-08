import json
import pandas as pd
import streamlit as st
from modules.auth import get_current_user, get_user
from modules.database import add_liked_game
from modules.utils import *

GAMES_PATH = "data/clusteredDataset.pkl"
N_OF_GAMES = 40

user = load_user()

st.set_page_config(layout="wide")
st.title("Choose your favorite games")

games_liked = get_games_liked(user)
df = load_games(GAMES_PATH)

if "grid_df" not in st.session_state:
    st.session_state.grid_df = get_top_games(df, N_OF_GAMES)
grid_df = st.session_state.grid_df

game_selections = render_game_grid(grid_df, games_liked)

if st.button("Submit"):
    process_selections(game_selections)
