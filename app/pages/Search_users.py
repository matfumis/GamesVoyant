import streamlit as st


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please log in to access this page.")
    st.stop()


st.title("Search Users")
