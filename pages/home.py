import streamlit as st
from modules.auth import get_current_user, logout

# Controlla subito se l'utente è autenticato; se non lo è, redireziona subito all'entry point dell'app
user = get_current_user()
if user is None:
    st.switch_page("app.py")
    stop()

st.title("Home")

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


st.header("A bunch of games that you may like:")