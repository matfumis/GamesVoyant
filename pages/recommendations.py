import streamlit as st
from modules.auth import get_current_user

user = get_current_user()
if not user:
    st.error("Non sei autenticato. Effettua il login.")
    st.stop()

st.title("Recommendations")
st.write("Ecco le tue raccomandazioni personalizzate...")
