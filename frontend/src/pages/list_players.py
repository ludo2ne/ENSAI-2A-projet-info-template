# frontend/pages/players.py
import logging
import time

import pandas as pd
import streamlit as st

from utils.api_client import api_client

st.title("Player list")

if not st.session_state.get("player"):
    logging.info("Not logged in, return to the home page")
    st.error("Access restricted to logged-in users.")
    time.sleep(1)
    st.switch_page("pages/home.py")

logging.info("Display players list")

players = api_client.get("/player").get("data")

if players:
    if isinstance(players, list):
        df = pd.DataFrame(players)
        if "password" in df.columns:
            df = df.drop(columns=["password"])
        st.dataframe(df)
    else:
        logging.info("No players found.")
        st.info("No players found.")


if st.button("Back to menu", type="primary"):
    logging.info("Back to homepage")
    st.switch_page("pages/player_menu.py")
