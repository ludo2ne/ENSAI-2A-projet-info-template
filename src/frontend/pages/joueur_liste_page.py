# frontend/pages/joueurs.py
import time

import pandas as pd
import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:5000")


st.title("📋 Liste des joueurs")

if st.session_state.get("joueur") is None:
    st.error("Accès non autorisé. Veuillez vous connecter.")
    time.sleep(1)
    st.switch_page("main_page.py")

if st.button("⬅️ Retour au menu"):
    st.switch_page("pages/menu_page.py")
try:
    r = requests.get(f"{API_URL}/joueur/")
    r.raise_for_status()
    joueurs = r.json()
    if isinstance(joueurs, list) and joueurs:
        df = pd.DataFrame(joueurs)
        df = df.drop(columns=["mdp"])
        st.dataframe(df)
    else:
        st.info("Aucun joueur trouvé.")
except requests.RequestException:
    st.error("Erreur de connexion au serveur API.")
