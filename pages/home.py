from modules.recommender import *
from modules.utils import *

st.set_page_config(layout="wide")

user = load_user()

st.title("Home")

custom_sidebar(user)

st.header("Games recommended to you:")

spacing()

display_games_in_grid(pick_recommended_games(get_current_user()["username"], 12), "recommended_to_you")
st.markdown("---")

st.header("Popular games you may like")

spacing()

display_games_in_grid(pick_popular_games(12), "popular")
st.markdown("---")

user = get_user(user['username'])
followed_users = get_followed_users(user)
selected_user = st.selectbox("Select one of your followed users:", followed_users)

if selected_user is not None:
    st.header(f"Games recommended to {selected_user}")
    display_games_in_grid(pick_recommended_games(selected_user, 12), f"recommended_to_followed_user")
    st.markdown("---")

spacing()
if st.button("Refresh Games"):
    st.rerun()
