from modules.auth import *
from modules.recommender import *
from modules.utils import *

# Controlla subito se l'utente è autenticato; se non lo è, redireziona subito all'entry point dell'app
user = get_current_user()
if user is None:
    st.switch_page("app.py")

st.title("Home")

# sidebar custom, serve per nascondere authentication.py e app.py a cui l'utente di fatto non serve mai accedere.
# Si aggiungono solo le pagine a cui l'utente può accedere
st.sidebar.page_link('pages/home.py', label='Home')
st.sidebar.page_link('pages/account.py', label='Personal Area')
with st.sidebar:
    st.write("")
    st.write("")
    st.info(f"Logged in as: {user['username']}")
    if st.button("Logout"):
        logout()
        st.switch_page("app.py")
"""
st.header("A bunch of games that you may like:")

current_dir = os.path.dirname(__file__)
pkl_path = os.path.join(current_dir, '..', 'data', 'clusteredDataset.pkl')
df = pd.read_pickle(pkl_path)

st.dataframe(df.head(50))
st.dataframe(pick_recommended_games("bob", 10))
"""

st.header("Games recommended for you")
display_games(pick_recommended_games(get_current_user()["username"], 10))

st.header("Popular games you may like")
display_games(pick_popular_games(10))

st.header("Games recommended to .....")
