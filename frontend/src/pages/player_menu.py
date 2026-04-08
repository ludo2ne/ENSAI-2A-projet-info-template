import logging
import time

import streamlit as st

player = st.session_state.get("player")

st.title("Main menu")

if not player:
    logging.info("Not logged in, return to the home page")
    st.error("Access restricted to logged-in users.")
    time.sleep(1)
    st.switch_page("pages/home.py")

st.badge(f"Hello {player['username']}!", color="green")

st.write("Available actions:")

if st.button("List all players"):
    logging.info("List all players")
    st.switch_page("pages/list_players.py")
if st.button(label="Play"):
    logging.info("Play games")
    st.switch_page("pages/play_game.py")
if st.button(label="Log out", type="primary"):
    logging.info("Log out")
    del st.session_state["player"]
    st.switch_page("pages/home.py")
