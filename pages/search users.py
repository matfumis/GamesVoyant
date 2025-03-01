import streamlit as st
from modules.auth import *
from modules.database import *
from modules.utils import *

st.set_page_config(layout="wide")
current_user = get_current_user()
if current_user is None:
    st.switch_page("app.py")

st.title("Search Users")
st.write("Find other users to follow!")

st.sidebar.page_link('pages/home.py', label='Home')
st.sidebar.page_link('pages/personal.py', label='Personal Area')
st.sidebar.page_link('pages/search users.py', label='Search Users')
with st.sidebar:
    st.write("")
    st.write("")
    st.info(f"Logged in as: {current_user['username']}")
    if st.button("Logout"):
        logout()
        st.switch_page("app.py")

search_query = st.text_input("Search by username, name or surname")

if st.button("Search"):
    results = search_users(search_query)
    followed_users = get_followed_users(current_user)
    if not results:
        st.info("User not found")
    else:
        st.markdown("---")

        for user in results:
            if user["user_id"] == current_user["user_id"]:
                continue

            info_col, action_col = st.columns([3, 1])
            with info_col:
                st.markdown(f"**Username:** {user['username']}")
                st.markdown(f"**Name:** {user['name']}")
                st.markdown(f"**Surname:** {user['surname']}")
                st.markdown(f"**Nationality:** {user['nationality']}")
                st.markdown(f"**Date of birth:** {user['date_of_birth']}")
            with action_col:
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
