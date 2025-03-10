from modules.utils import *

st.set_page_config(layout="wide")
current_user = get_current_user()
if current_user is None:
    st.switch_page("app.py")

current_user = get_user(current_user["username"])

st.title("Search Users")
st.write("Find other users to follow!")

custom_sidebar(current_user)

search_query = st.text_input("Search by username, name or surname")

if search_query:
    results = search_users(search_query)
else:
    results = search_users("")

if not results:
    st.info("User not found")
else:
    display_users(results, get_user(current_user['username']))
