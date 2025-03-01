import streamlit as st
import json
import pandas as pd
from modules.auth import get_current_user, logout, get_user

# Ensure the user is logged in.
current_user = get_current_user()
if current_user is None:
    st.switch_page("app.py")
    st.stop()

# Check that a profile user is stored in session_state.
if "profile_user" not in st.session_state:
    st.info("No profile selected, redirecting to Personal Area.")
    st.switch_page("personal")
    st.stop()

profile_user = st.session_state.profile_user

st.title(f"Profile: {profile_user['username']}")

# Sidebar for navigation.
st.sidebar.page_link('pages/home.py', label='Home')
st.sidebar.page_link('pages/personal.py', label='Personal Area')
with st.sidebar:
    st.write("")
    st.write("")
    st.info(f"Logged in as: {current_user['username']}")
    if st.button("Logout"):
        logout()
        st.switch_page("app.py")

st.markdown("---")

# Display a profile image (using RoboHash as a placeholder).
default_user_icon = f"https://robohash.org/{profile_user['username']}?set=set1"
st.image(default_user_icon, width=150)

# Display user details.
st.header(f"{profile_user.get('name', '')} {profile_user.get('surname', '')}")
st.subheader(f"Username: {profile_user['username']}")
st.write(f"Nationality: {profile_user.get('nationality', 'N/A')}")
st.write(f"Date of Birth: {profile_user.get('date_of_birth', 'N/A')}")

if profile_user.get("saved_games"):
    st.write("Saved Games:", profile_user["saved_games"])


user_saved_games = profile_user.get("saved_games", "[]")
if isinstance(user_saved_games, str):
    user_saved_games = json.loads(user_saved_games)

games_df = pd.read_pickle("data/clusteredDataset.pkl")
user_saved_games_df = games_df[games_df["AppID"].isin(user_saved_games)]

user_id = st.session_state.user.get("user_id")
num_columns = 3
saved_games_list = user_saved_games_df.to_dict('records')

if not saved_games_list:
    st.info("No saved games found.")
else:
    for i in range(0, len(saved_games_list), num_columns):
        cols = st.columns(num_columns)
        for j, game in enumerate(saved_games_list[i:i+num_columns]):
            with cols[j]:
                if game.get("Header image"):
                    st.image(game["Header image"], use_column_width=True)
                    st.markdown(f"""
                        <div style="height:120px; overflow-y:auto">
                            <h4 style="margin-bottom: 0.25rem;">{game["Name"]}</h4>
                            <p style="color: gray; margin-top: 0rem;">Release: {game["Release date"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    app_id = game.get("AppID", None)

st.markdown("---")

# Button to return to the personal area.
if st.button("Back to Personal Area"):
    st.switch_page("pages/personal.py")
