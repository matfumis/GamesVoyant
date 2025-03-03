from modules.auth import *
from modules.recommender import *
from modules.utils import *

st.set_page_config(layout="wide")

user = get_current_user()
if user is None:
    st.switch_page("app.py")

st.title("Home")

st.sidebar.page_link('pages/home.py', label='Home')
st.sidebar.page_link('pages/personal.py', label='Personal Area')
st.sidebar.page_link('pages/search users.py', label='Search Users')
with st.sidebar:
    st.write("")
    st.write("")
    st.info(f"Logged in as: {user['username']}")
    if st.button("Logout"):
        logout()
        st.switch_page("app.py")

st.header("Games recommended to you")
display_games_in_grid(pick_recommended_games(get_current_user()["username"], 12), "recommended_to_you")
st.markdown("---")

st.header("Popular games you may like")
display_games_in_grid(pick_popular_games(12), "popular")
st.markdown("---")

user = get_user(user['username'])
followed_users = get_followed_users(user)
selected_user = st.selectbox("Select one of your followed users:", followed_users)

if selected_user is not None:
    st.header(f"Games recommended to {selected_user}")
    display_games_in_grid(pick_recommended_games(selected_user, 12), f"recommended_to_followed_user")
    st.markdown("---")
