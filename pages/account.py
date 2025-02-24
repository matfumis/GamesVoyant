import streamlit as st
from modules.auth import *
import pandas as pd

user = get_current_user()
if user is None:
    st.switch_page("app.py")
    stop()

st.title("Personal Area")

# sidebar custom, serve per nascondere authentication.py e app.py a cui l'utente di fatto non serve mai accedere.
# Si aggiungono solo le pagine a cui l'utente può accedere
st.sidebar.page_link('pages/home.py', label='Home')
st.sidebar.page_link('pages/account.py', label='Personal Area')
with st.sidebar:
    st.write("")
    st.write("")
    st.info(f"Logged in as: {user['username']}")
    if st.button("Logout"):
        logout()
        st.switch_page("app.py")

st.header(f"Welcome, {user['username']}")

st.markdown("---")

st.header("Your saved games")
st.write(user['saved_games'])

st.markdown("---")

st.header("Followed users")


