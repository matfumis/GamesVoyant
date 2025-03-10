import json
import pandas as pd
import streamlit as st
from modules.auth import get_current_user, get_user
from modules.database import add_liked_game
from modules.utils import *
from modules.recommender import *

N_OF_GAMES = 40

user = load_user()

st.set_page_config(layout="wide")
st.title("Choose your favorite games")

spacing()

games_liked = json.loads(user["games_liked"])
df = get_dataframe()

if "grid_df" not in st.session_state:
    st.session_state.grid_df = pick_popular_games(N_OF_GAMES)
grid_df = st.session_state.grid_df

game_selections = render_game_grid(grid_df, games_liked)

if st.button("Submit"):
    process_selections(game_selections)
