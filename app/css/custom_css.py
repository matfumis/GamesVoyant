import streamlit as st

def hide_sidebar():
    hide_css = """
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    button[aria-label="Toggle sidebar"],
    header [data-testid="stSidebarToggle"] {
        display: none !important;
    }
    """
    st.markdown(hide_css, unsafe_allow_html=True)
