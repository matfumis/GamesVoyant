import pandas as pd
from modules.utils import *

user = load_user();

if "profile_user" not in st.session_state:
    st.info("No profile selected, redirecting to Personal Area.")
    st.switch_page("personal")

profile_user = st.session_state.profile_user

st.title(f"Profile: {profile_user['username']}")
custom_sidebar(get_current_user())
st.markdown("---")

default_user_icon = f"https://robohash.org/{profile_user['username']}?set=set1"
st.image(default_user_icon, width=150)

st.header(f"{profile_user.get('name', '')} {profile_user.get('surname', '')}")
st.subheader(f"Username: {profile_user['username']}")
st.write(f"Nationality: {profile_user.get('nationality', 'N/A')}")
st.write(f"Date of Birth: {profile_user.get('date_of_birth', 'N/A')}")

show_user_saved_games(profile_user)
st.markdown("---")

if st.button("Back"):
    st.switch_page("pages/search_users.py")
