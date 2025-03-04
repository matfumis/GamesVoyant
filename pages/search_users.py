import streamlit as st
from modules.auth import *
from modules.database import *
from modules.utils import *

st.set_page_config(layout="centered")
current_user = get_current_user()
if current_user is None:
    st.switch_page("app.py")

current_user = get_user_by_id(current_user["user_id"])

st.title("Search Users")
st.write("Find other users to follow!")

custom_sidebar(current_user)

search_query = st.text_input("Search by username, name or surname")

if search_query:
    results = search_users(search_query)
else:
    results = search_users("")

current_user = get_user(current_user['username'])
followed_users = get_followed_users(current_user)

if not results:
    st.info("User not found")
else:
    st.markdown("---")

    for user in results:
        if user["user_id"] == current_user["user_id"]:
            continue

        col_image, col_info, col_view, col_follow = st.columns([1, 1, 1, 1])

        with col_image:
            default_user_icon = f"https://robohash.org/{user['username']}?set=set1"
            st.image(default_user_icon, width=100)

        with col_info:
            st.markdown(f"**Username:** {user['username']}")

        with col_view:
            if st.button("View Profile", key=f"view_{user['user_id']}"):
                st.session_state.profile_user = user
                st.switch_page("pages/user_profile.py")

        with col_follow:
            followed = user["username"] in followed_users
            if followed:
                st.button(
                    "Unfollow",
                    key=f"unfollow_{user['user_id']}",
                    on_click=remove_follow,
                    args=(current_user["user_id"], user["user_id"])
                )
            else:
                st.button(
                    "Follow",
                    key=f"follow_{user['user_id']}",
                    on_click=add_follow,
                    args=(current_user["user_id"], user["user_id"])
                )

        st.markdown("---")
