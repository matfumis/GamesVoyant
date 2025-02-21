import streamlit as st
from modules.auth import get_current_user

user = get_current_user()
if not user:
    st.error("Non sei autenticato. Effettua il login.")
    st.stop()

st.title("Home Page")
st.write(f"Benvenuto, {user['username']}!")
