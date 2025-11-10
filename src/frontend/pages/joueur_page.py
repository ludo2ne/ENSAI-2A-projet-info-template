# frontend/pages/joueurs.py
import pandas as pd
import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:8000")


def joueurs_page():
    st.header("Liste des joueurs")
    if "user" not in st.session_state:
        st.warning(
            "Veuillez vous connecter depuis l'onglet 'Connexion' avant d'accéder à la liste."
        )
        return

    if st.button("Rafraîchir"):
        pass

    try:
        r = requests.get(f"{API_URL}/joueurs/", timeout=5)
    except requests.RequestException as exc:
        st.error(f"Erreur réseau : {exc}")
        return

    if r.status_code == 200:
        joueurs = r.json()
        # Convertir en DataFrame pour afficher proprement
        if isinstance(joueurs, list):
            df = pd.DataFrame(joueurs)
            st.table(df)
        else:
            st.write(joueurs)
    else:
        st.error(f"Erreur serveur : {r.status_code}")
