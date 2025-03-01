from modules.auth import *
from modules.recommender import *
from modules.utils import *

st.set_page_config(layout="wide")
# Controlla subito se l'utente è autenticato; se non lo è, redireziona subito all'entry point dell'app
user = get_current_user()
if user is None:
    st.switch_page("app.py")

st.title("Home")

# sidebar custom, serve per nascondere authentication.py e app.py a cui l'utente di fatto non serve mai accedere.
# Si aggiungono solo le pagine a cui l'utente può accedere
st.sidebar.page_link('pages/home.py', label='Home')
st.sidebar.page_link('pages/personal.py', label='Personal Area')
with st.sidebar:
    st.write("")
    st.write("")
    st.info(f"Logged in as: {user['username']}")
    if st.button("Logout"):
        logout()
        st.switch_page("app.py")

st.header("Games recommended for you")
display_games_in_grid(pick_recommended_games(get_current_user()["username"], 12), "recommended4you")
st.markdown("---")

st.header("Popular games you may like")
display_games_in_grid(pick_popular_games(12), "popular")
st.markdown("---")

st.header("Games recommended to .....")
