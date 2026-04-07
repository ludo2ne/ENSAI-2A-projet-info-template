# frontend/pages/joueurs.py
import logging
import time

import pandas as pd
import streamlit as st

from utils.api_client import api_client

st.title("📋 Liste des joueurs")

if st.session_state.get("joueur") is None:
    st.error("Accès non autorisé. Veuillez vous connecter.")
    time.sleep(1)
    st.switch_page("pages/main_page.py")

if st.button("⬅️ Retour au menu"):
    st.switch_page("pages/menu_page.py")

joueurs = api_client.get("/joueur").get("data")

if joueurs:
    logging.info(joueurs)
    if isinstance(joueurs, list):
        df = pd.DataFrame(joueurs)
        if "mdp" in df.columns:
            df = df.drop(columns=["mdp"])
        st.dataframe(df)
    else:
        st.info("Aucun joueur trouvé.")
