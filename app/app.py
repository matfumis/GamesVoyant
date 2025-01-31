import datetime
import jwt
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import sys

from authentication import login_user, signup_user
import personal_area
import search_users
import search_games

SECRET_KEY = "YOUR_SUPER_SECRET_KEY"

def generate_jwt_token(user_dict, expires_minutes=1440):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    payload = {
        "exp": expiry,
        "user": user_dict,  
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
        


def main():
    st.set_page_config(page_title="GamesVoyant", layout="wide")

    cookies = EncryptedCookieManager(prefix="gamesvoyant_", password="CHANGE_ME")  
    if not cookies.ready():
        st.stop()

    token_from_cookie = cookies.get("auth_token")
    if token_from_cookie:
        payload = decode_jwt_token(token_from_cookie)
        if payload is not None:
            if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
                st.session_state["authenticated"] = True
                st.session_state["user"] = payload["user"]
        else:
            cookies["auth_token"] = ""
            cookies.save()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.authenticated:

        st.title("GamesVoyant :crystal_ball::space_invader:")
        st.header("A world of endless adventures awaits you...")

        tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])
        
        # === LOGIN TAB ===
        with tab_login:
            st.header("Log In")
            username_login = st.text_input("Username", key="username_login")
            password_login = st.text_input("Password", type="password", key="password_login")
            
            if st.button("Log In"):
                user = login_user(username_login, password_login)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "user_id": user["user_id"],
                        "username": user["username"],
                        "name": user["name"],
                    }

                    token = generate_jwt_token(st.session_state.user, expires_minutes=1440)
                    cookies["auth_token"] = token
                    cookies.save()

                    st.rerun() 
                else:
                    st.error("Invalid username or password")
        
        # === SIGNUP TAB ===
        with tab_signup:
            st.header("Sign Up")
            username_signup = st.text_input("Username", key="username_signup")
            name_signup = st.text_input("Name", key="name_signup")
            surname_signup = st.text_input("Surname", key="surname_signup")
            nationality_signup = st.text_input("Nationality", key="nationality_signup")
            date_of_birth_signup = st.date_input("Date of birth", key="dob_signup")
            password_signup = st.text_input("Password", type="password", key="password_signup")
            password_confirm_signup = st.text_input("Confirm Password", type="password", key="password_confirm_signup")
            
            if st.button("Sign Up"):
                if password_signup == password_confirm_signup:
                    success, msg = signup_user(
                        username_signup,
                        password_signup,
                        name_signup,
                        surname_signup,
                        nationality_signup,
                        date_of_birth_signup
                    )
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.error("Passwords do not match!")
    
    else:
        st.title("GamesVoyant :crystal_ball::space_invader:")
        
        # === SIDEBAR ===
        choice = st.sidebar.radio("Navigate", ["Personal Area", "Search Users", "Search Videogames"])
        
        if choice == "Personal Area":
            personal_area.show()
        elif choice == "Search Users":
            search_users.show()
        elif choice == "Search Videogames":
            search_games.show()
        
        # === LOGOUT BUTTON ===
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None

            cookies["auth_token"] = ""
            cookies.save()

            st.rerun()


if __name__ == "__main__":
    main()
