# frontend/pages/joueurs.py
import time

import pandas as pd
import streamlit as st

from utils.api_client import api_client

st.title("Player list")

if not st.session_state.get("joueur"):
    st.error("Access restricted to logged-in users.")
    time.sleep(1)
    st.switch_page("pages/home.py")

joueurs = api_client.get("/joueur").get("data")

if joueurs:
    if isinstance(joueurs, list):
        df = pd.DataFrame(joueurs)
        if "mdp" in df.columns:
            df = df.drop(columns=["mdp"])
        st.dataframe(df)
    else:
        st.info("No players found.")


if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")
