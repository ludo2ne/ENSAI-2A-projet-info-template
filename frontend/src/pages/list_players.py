# frontend/pages/joueurs.py
import logging
import time

import pandas as pd
import streamlit as st

from utils.api_client import api_client

st.title("Player list")

if not st.session_state.get("joueur"):
    logging.info("Not logged in, return to the home page")
    st.error("Access restricted to logged-in users.")
    time.sleep(1)
    st.switch_page("pages/home.py")

logging.info("Display players list")

joueurs = api_client.get("/joueur").get("data")

if joueurs:
    if isinstance(joueurs, list):
        df = pd.DataFrame(joueurs)
        if "mdp" in df.columns:
            df = df.drop(columns=["mdp"])
        st.dataframe(df)
    else:
        logging.info("No players found.")
        st.info("No players found.")


if st.button("Back to menu", type="primary"):
    logging.info("Back to homepage")
    st.switch_page("pages/player_menu.py")
