import streamlit as st
from modules.auth import get_current_user
from modules.database import search_users, add_follow, remove_follow

current_user = get_current_user()
if not current_user:
    st.error("Non sei autenticato. Effettua il login.")
    st.stop()

st.title("Search Users")
st.write("Find other users to follow!")

search_query = st.text_input("Cerca per username, nome o cognome")

if st.button("Cerca"):
    results = search_users(search_query)
    if not results:
        st.info("Nessun utente trovato.")
    else:
        st.write("Risultati della ricerca:")
        for user in results:
            if user["user_id"] == current_user["user_id"]:
                continue

            info_col, action_col = st.columns([3, 1])
            with info_col:
                st.markdown(f"**Username:** {user['username']}")
                st.markdown(f"**Nome:** {user['name']}")
                st.markdown(f"**Cognome:** {user['surname']}")
                st.markdown(f"**Nazionalità:** {user['nationality']}")
                st.markdown(f"**Data di nascita:** {user['date_of_birth']}")
            with action_col:
                followed = False
                if "followed_users" in current_user and current_user["followed_users"]:
                    followed = user["user_id"] in current_user["followed_users"]

                if followed:
                    if st.button("Non Seguire", key=f"unfollow_{user['user_id']}"):
                        add_follow(current_user["user_id"], user["user_id"])
                else:
                    if st.button("Segui", key=f"follow_{user['user_id']}"):
                        remove_follow(current_user["user_id"], user["user_id"])
