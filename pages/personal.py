import pandas as pd
from modules.utils import *
from modules.recommender import *

user = load_user();

st.title("Personal Area")
custom_sidebar(user)
st.header(f"Welcome, {user['username']}")
st.markdown("---")

st.header("Your saved games")

show_user_saved_games(user)
st.markdown("---")

st.header("Followed users")

show_followed_users(get_followed_users(user))
st.markdown("---")

st.write(
    "In any moment, you can choose to reset your preferences and start over the preferences calibration like the first time you registered:")
if st.button("Reset preferences"):
    games_liked = json.loads(user["games_liked"])
    games_disliked = json.loads(user["games_disliked"])
    for game in games_liked:
        remove_liked_game(user["user_id"], game)
    for game in games_disliked:
        remove_disliked_game(user["user_id"], game)
    st.switch_page("pages/calibration.py")
