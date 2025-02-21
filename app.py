from modules.auth import get_current_user
import streamlit as st

st.set_page_config(
    page_title="GamesVoyant",
    layout="centered",
    initial_sidebar_state="expanded",
)

user = get_current_user()

if user is None:
    st.switch_page("pages/authentication.py")
else:
    st.switch_page("pages/home.py")