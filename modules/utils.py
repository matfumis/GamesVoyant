import streamlit as st
from modules.database import *
from modules.auth import *


def display_games_in_grid(df, prefix):
    num_rows = 3
    num_cols = 4
    user = get_current_user()
    for row_idx in range(num_rows):
        columns = st.columns(num_cols)

        start_idx = row_idx * num_cols
        end_idx = start_idx + num_cols
        row_games = df.iloc[start_idx:end_idx]

        for col_idx, (_, game) in enumerate(row_games.iterrows()):
            with columns[col_idx]:
                st.markdown(f"#### {game['Name']}")
                st.write(f"**Release Date:** {game['Release date']}")
                st.image(game["Header image"], width=200)
                st.write(f"**Price:** {game['Price']}")

                like_button = st.button("Like", key=f"{prefix}_like_{start_idx + col_idx}")
                dislike_button = st.button("Dislike", key=f"{prefix}_dislike_{start_idx + col_idx}")
                save_button = st.button("Save", key=f"{prefix}_save_{start_idx + col_idx}")

                if like_button:
                    add_liked_game(user['user_id'], game["AppID"])
                if dislike_button:
                    add_disliked_game(user['user_id'], game["AppID"])
                if save_button:
                    add_saved_game(user['user_id'], game["AppID"])
