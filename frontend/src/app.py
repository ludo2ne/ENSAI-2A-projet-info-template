import streamlit as st

from utils.log_init import initialize_logs

if "logs_initialized" not in st.session_state:
    initialize_logs("Streamlit App")
    st.session_state["logs_initialized"] = True

if "player" in st.session_state:
    st.switch_page("pages/player_menu.py")
else:
    st.switch_page("pages/home.py")
