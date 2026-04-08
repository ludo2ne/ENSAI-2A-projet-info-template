import time

import streamlit as st

joueur = st.session_state.get("joueur")

st.title("Main menu")

if not joueur:
    st.error("Access restricted to logged-in users.")
    time.sleep(1)
    st.switch_page("pages/home.py")

st.badge(f"Hello {joueur['pseudo']}!", color="green")

st.write("Available actions:")

if st.button("List all players"):
    st.switch_page("pages/list_players.py")
if st.button(label="Play"):
    st.switch_page("pages/play_game.py")
if st.button(label="Log out", type="primary"):
    del st.session_state["joueur"]
    st.switch_page("pages/home.py")
