from modules.auth import *

st.set_page_config(
    page_title="Steam Game Recommender",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
)

st.title("Autenticazione")

if st.session_state.get("login_success", False):
    st.success("Login effettuato con successo!")

if st.session_state.get("signup_success", False):
    st.success("Registrazione avvenuta con successo! Ora puoi effettuare il login.")

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = None

if st.session_state.auth_mode is None:
    if st.button("Accedi", key="btn_accedi"):
        st.session_state.auth_mode = "login"
        st.rerun()
    if st.button("Registrati", key="btn_registrati"):
        st.session_state.auth_mode = "register"
        st.rerun()

if st.session_state.auth_mode == "login":
    st.subheader("Effettua il Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Invia", key="btn_invia_login"):
        if login(username, password):
            st.session_state.login_success = True
            st.session_state.signup_success = False
            st.rerun()

elif st.session_state.auth_mode == "register":
    st.subheader("Registrazione")
    username = st.text_input("Scegli un username", key="reg_username")
    password = st.text_input("Scegli una password", type="password", key="reg_password")
    name = st.text_input("Nome", key="reg_name")
    surname = st.text_input("Cognome", key="reg_surname")
    nationality = st.text_input("Nazionalità", key="reg_nationality")
    date_of_birth = st.date_input("Data di Nascita", key="reg_date_of_birth")
    if st.button("Registrati", key="btn_invia_reg"):
        if not username.strip():
            st.error("Il campo username non può essere vuoto.")
        if len(password) < 6:
            st.error("La password deve contenere almeno 6 caratteri.")
        if not name.strip():
            st.error("Il campo Nome non può essere vuoto.")
        if not surname.strip():
            st.error("Il campo Cognome non può essere vuoto.")

        if register(username, password, name, surname, nationality, date_of_birth):
            st.session_state.signup_success = True
            st.session_state.login_success = False
            st.session_state.auth_mode = "login"
            st.rerun()

if st.session_state.auth_mode is not None:
    if st.button("Indietro", key="btn_indietro"):
        st.session_state.auth_mode = None
        st.rerun()
