import bcrypt
from modules.database import *


def register(username, password, name, surname, nationality, date_of_birth):
    if get_user(username) is not None:
        st.error("Username already exists")
        return False

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        add_user(username, password_hash, name, surname, nationality, date_of_birth)
        return True
    except Exception as e:
        st.error(f"Error during registration: {e}")
        return False


def login(username, password):
    user = get_user(username)
    if user is None:
        st.error("User not found")
        return False

    stored_hash = user["password_hash"].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        st.session_state.user = user
        return True
    else:
        st.error("Incorrect password")
        return False


def logout():
    st.session_state.user = None


def get_current_user():
    return st.session_state.get("user", None)
