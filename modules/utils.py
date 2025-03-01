import streamlit as st
from modules.database import *
from modules.auth import *
import json


def get_followed_users(user):
    followed_users_ids = json.loads(user["followed_users"])
    followed_users_usernames = []
    for user_id in followed_users_ids:
        username = get_username(user_id)
        followed_users_usernames.append(username)
    return followed_users_usernames


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
                # st.markdown(f"#### {game['Name']}")
                # st.write(f"**Release Date:** {game['Release date']}")
                st.image(game["Header image"], use_column_width=True)
                #  st.write(f"**Price:** {game['Price']}")

                st.markdown(f"""
                        <div style="height:120px; overflow-y:auto">
                            <h4 style="margin-bottom: 0.25rem;">{game["Name"]}</h4>
                            <p style="color: gray; margin-top: 0rem;">Release: {game["Release date"]}</p>
                            <p style="color: gray; margin-top: 0rem;">Price: {game["Price"]}</p>
                        </div>
                    """, unsafe_allow_html=True)

                app_id = game["AppID"]

                st.button("Like", key=f"{prefix}_like_{start_idx + col_idx}",
                          on_click=add_liked_game, args=(user['user_id'], app_id))
                st.button("Dislike", key=f"{prefix}_dislike_{start_idx + col_idx}",
                          on_click=add_disliked_game, args=(user['user_id'], app_id))
                st.button("Save", key=f"{prefix}_save_{start_idx + col_idx}",
                          on_click=add_saved_game, args=(user['user_id'], app_id))
