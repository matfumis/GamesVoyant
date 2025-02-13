import streamlit as st
import pandas as pd
from database import *

def show_select_games():
    st.title("Select Your Favorite Games")
    st.write("As part of the registration process, please select between **1 and 3 games** that interest you.")

    if "random_games_df" not in st.session_state:
        df_games = load_random_games(limit=10)
        st.session_state["random_games_df"] = df_games
    else:
        df_games = st.session_state["random_games_df"]

    selected_games = []
    cols = st.columns(2)
    for idx, row in df_games.iterrows():
        col = cols[idx % 2]
        with col:
            # Display a placeholder image.
            st.image("https://via.placeholder.com/150", width=150)
            st.subheader(row["Name"])
            st.caption(f"Release: {row['Release date']}")

            if st.checkbox("Select", key=f"game_{row['Name']}"):
                selected_games.append(row["Name"])

    if st.button("Submit Selection"):
        if not (1 <= len(selected_games) <= 3):
            st.error("Please select between 1 and 3 games.")
        else:
            if "user" not in st.session_state or not st.session_state.user or "user_id" not in st.session_state.user:
                st.error("User session not found. Please log in again.")
                return

            user_id = st.session_state.user["user_id"]

            update_user_games_liked(user_id, selected_games)

            st.session_state.selected_games = selected_games
            st.success("Thank you for your selection!")

            st.session_state.show_select_games = False

            if "random_games_df" in st.session_state:
                del st.session_state["random_games_df"]

            st.rerun()

