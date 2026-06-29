"""
Streamlit page for the main player menu.

Provides navigation to available actions such as listing players or playing games for logged-in users.
"""

import logging

import streamlit as st

from utils.auth_guard import check_authentification

st.title("Main menu")
logging.info("Player menu")

check_authentification()

player = st.session_state.get("player")

st.badge(f"Hello {player['username']}!", color="green")

st.write("Available actions:")

if st.button("List all players"):
    st.switch_page("pages/list_players.py")
if st.button(label="Play"):
    st.switch_page("pages/play_game.py")
if st.button(label="Log out", type="primary"):
    logging.info("Log out")
    del st.session_state["player"]
    st.switch_page("pages/home.py")
