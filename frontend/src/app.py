import streamlit as st

from utils.log_init import initialiser_logs

initialiser_logs("Streamlit App")

st.markdown(
    """
    <style>
    div[data-baseweb="notification"] {
        background-color: #ffe6e6 !important;
        color: #000000 !important;
        border: 1px solid red;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "joueur" in st.session_state:
    st.switch_page("pages/player_menu.py")
else:
    st.switch_page("pages/home.py")
