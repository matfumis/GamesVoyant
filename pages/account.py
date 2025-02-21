import streamlit as st
from modules.auth import get_current_user

user = get_current_user()
if not user:
    st.error("Non sei autenticato. Effettua il login.")
    st.stop()

st.title("Area Personale")
st.write(f"**Username:** {user['username']}")
st.write(f"**Nome:** {user['name']}")
st.write(f"**Cognome:** {user['surname']}")
st.write(f"**Nazionalità:** {user['nationality']}")
st.write(f"**Data di nascita:** {user['date_of_birth']}")
