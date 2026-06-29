"""
Streamlit page for listing all players.

Retrieves and displays a list of registered players in a table, excluding sensitive data like passwords.

Endpoint used:
    GET /player
"""

import logging

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification

st.title("Player list")
logging.info("List all players")

check_authentification()

logging.info("Display players list")

players = api_client.get("/player").get("data")

if players:
    if isinstance(players, list):
        df = pd.DataFrame(players)
        st.dataframe(df, hide_index=True)
    else:
        logging.info("No players found.")
        st.info("No players found.")


if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")
