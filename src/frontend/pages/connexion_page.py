import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:8000")


def connexion_page():
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        try:
            r = requests.post(
                f"{API_URL}/joueurs/connexion",
                json={"username": username, "password": password},
                timeout=5,
            )
        except requests.RequestException as exc:
            st.error(f"Erreur réseau : {exc}")
            return

        if r.status_code == 200:
            st.success("Connexion réussie")
            st.session_state["user"] = r.json()
        elif r.status_code == 401:
            st.error("Identifiants incorrects")
        else:
            st.error(f"Erreur serveur ({r.status_code})")
