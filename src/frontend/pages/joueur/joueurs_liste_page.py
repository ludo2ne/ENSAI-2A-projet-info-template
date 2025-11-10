# frontend/pages/joueurs.py
import pandas as pd
import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:5000")


def joueurs_liste_page():
    st.title("📋 Liste des joueurs")

    if st.button("⬅️ Retour au menu"):
        st.session_state["page"] = "menu"
        st.rerun()

    try:
        r = requests.get(f"{API_URL}/joueur/")
        r.raise_for_status()
        joueurs = r.json()
        if isinstance(joueurs, list) and joueurs:
            df = pd.DataFrame(joueurs)
            st.dataframe(df)
        else:
            st.info("Aucun joueur trouvé.")
    except requests.RequestException:
        st.error("Erreur de connexion au serveur API.")
