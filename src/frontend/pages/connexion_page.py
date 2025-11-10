import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:5000")


def connexion_page():
    st.title("🔐 Connexion")

    pseudo = st.text_input("Pseudo")
    mdp = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        try:
            r = requests.post(f"{API_URL}/connexion", json={"pseudo": pseudo, "mdp": mdp})
        except requests.RequestException:
            st.error("Erreur de connexion au serveur API.")
            return

        if r.status_code == 200:
            joueur = r.json()
            st.session_state["joueur"] = joueur
            st.success(f"Bienvenue {joueur['pseudo']} ! 🎉")
            st.session_state.go_to("menu")
        elif r.status_code == 401:
            st.error("Identifiants incorrects ❌")
        else:
            st.error(f"Erreur serveur : {r.status_code}")
