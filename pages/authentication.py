import streamlit as st
import datetime
from modules.auth import *

if get_current_user() is not None:
    st.switch_page("pages/home.py")
    st.stop()

st.title("Authentication")

tab_login, tab_register = st.tabs(["Log In", "Register"])

with tab_login:
    col_left, col_mid, col_right = st.columns([1,4,1])
    with col_mid: 
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Submit", key="btn_login"):
            if login(username, password):
                st.rerun() 

with tab_register:
    col_left, col_mid, col_right = st.columns([1,4,1])
    with col_mid:
        st.subheader("Register")
        username = st.text_input("Username", key="reg_username")
        password = st.text_input("Password", type="password", key="reg_password")
        password_confirm = st.text_input("Confirm Password", type="password", key="password_confirm")
        name = st.text_input("Name", key="reg_name")
        surname = st.text_input("Surname", key="reg_surname")
        nationality = st.text_input("Nationality", key="reg_nationality")
        date_of_birth = st.date_input("Date of Birth", key="reg_date_of_birth",
                                    min_value=datetime.date(1925, 1, 1),
                                    max_value=datetime.date.today())
        if st.button("Register", key="btn_register"):
            if not username.strip():
                st.error("Username cannot be empty.")
            elif len(password) < 6:
                st.error("Password must be at least 8 characters.")
            elif password != password_confirm:
                st.error("Passwords do not match!")
            elif not name.strip():
                st.error("Name cannot be empty.")
            elif not surname.strip():
                st.error("Surname cannot be empty.")
            else:
                if register(username, password, name, surname, nationality, date_of_birth):
                    st.success("Registration successful! Now you can log in.")
                    login(username, password)
                    st.switch_page("pages/calibration.py")




