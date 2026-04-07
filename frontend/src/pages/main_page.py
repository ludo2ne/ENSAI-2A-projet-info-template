import streamlit as st

from utils.api_client import api_client

st.set_page_config(page_title="Gestion des joueurs", page_icon="🎮", layout="centered")

st.markdown(
    """
    <div style="text-align:center">
        <h1 style="color:#4B9CD3">Gestion des joueurs</h1>
        <p>Bienvenue</p>
    </div>
    """,
    unsafe_allow_html=True,
)

pseudo = st.text_input("Pseudo", placeholder="Entrez votre pseudo")
mdp = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")

with st.container(horizontal_alignment="center"):
    if st.button("Se connecter"):
        response = api_client.post("/connexion", json={"pseudo": pseudo, "mdp": mdp})

        if response:
            if response["status_code"] == 200:
                joueur = response["data"]
                st.session_state["joueur"] = joueur
                st.success(f"Bienvenue {joueur['pseudo']} ! 🎉")
                st.switch_page("pages/menu_page.py")
            elif response["status_code"] == 401:
                st.error("Identifiants incorrects ❌")
            else:
                st.error(f"Erreur serveur : {response['data']}")

st.space("small")

if st.button("➕ Créer un compte"):
    st.switch_page("pages/joueur_creation_page.py")

if st.button("Réinitialiser la base de données"):
    response = api_client.get("/reset_database")

    if response:
        st.success("Base de données réinitialisée ✅")
