import datetime
import jwt
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import sys

from authentication import login_user, signup_user
import personal_area
import search_users
import search_games

# === CONFIGURE YOUR SECRET KEY HERE ===
# In production, keep this secret safe (e.g., in environment variables).
SECRET_KEY = "YOUR_SUPER_SECRET_KEY"

# 1) Functions to generate & decode JWT tokens
def generate_jwt_token(user_dict, expires_minutes=1440):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    payload = {
        "exp": expiry,
        "user": user_dict,  # embed your user object
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
    st.set_page_config(page_title="Videogames Suggestion", layout="wide")

    # 2) Create (or load) an EncryptedCookieManager
    #    The prefix and password can be customized or read from environment variables.
    cookies = EncryptedCookieManager(prefix="gamesvoyant_", password="CHANGE_ME")  
    if not cookies.ready():
        # If cookies are not ready, stop execution to load them
        st.stop()

    # 3) Try to read the JWT token from the cookies on every run
    token_from_cookie = cookies.get("auth_token")
    if token_from_cookie:
        payload = decode_jwt_token(token_from_cookie)
        if payload is not None:
            # Token is valid -> user is considered authenticated
            if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
                st.session_state["authenticated"] = True
                st.session_state["user"] = payload["user"]
        else:
            # Token invalid or expired -> remove it
            cookies["auth_token"] = ""
            cookies.save()

    # 4) Initialize session state if missing
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None

    # 5) If not authenticated, show login/signup tabs
    if not st.session_state.authenticated:
        tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])
        
        # === LOGIN TAB ===
        with tab_login:
            st.header("Log In")
            username_login = st.text_input("Username", key="username_login")
            password_login = st.text_input("Password", type="password", key="password_login")
            
            if st.button("Log In"):
                user = login_user(username_login, password_login)
                if user:
                    # Mark session as authenticated
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "user_id": user["user_id"],
                        "username": user["username"],
                        "name": user["name"],
                        # Add more fields if needed...
                    }

                    # === Generate JWT and store in the cookie ===
                    token = generate_jwt_token(st.session_state.user, expires_minutes=1440)
                    cookies["auth_token"] = token
                    cookies.save()

                    st.rerun() # Reload the page to reflect changes
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
    
    # 6) If the user is authenticated, show the main content and sidebar
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

            # Clear the cookie
            cookies["auth_token"] = ""
            cookies.save()

            st.rerun()


if __name__ == "__main__":
    main()
