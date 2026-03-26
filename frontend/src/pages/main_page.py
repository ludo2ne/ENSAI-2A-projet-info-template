import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

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
mdp = st.text_input(
    "Mot de passe", type="password", placeholder="Entrez votre mot de passe"
)

with st.container(horizontal_alignment="center"):
    if st.button("Se connecter"):
        try:
            r = requests.post(
                f"{API_URL}/connexion", json={"pseudo": pseudo, "mdp": mdp}
            )
        except requests.RequestException:
            st.error("Erreur de connexion au serveur API.")
        if r.status_code == 200:
            joueur = r.json()
            st.session_state["joueur"] = joueur
            st.success(f"Bienvenue {joueur['pseudo']} ! 🎉")
            st.switch_page("pages/menu_page.py")
        elif r.status_code == 401:
            st.error("Identifiants incorrects ❌")
        else:
            try:
                error_detail = r.json().get("detail", r.text)
            except ValueError:
                error_detail = r.text
            st.error(
                f"Erreur serveur.  \nStatut : {r.status_code}  \nDétail : {error_detail}"
            )
st.space("small")

if st.button("➕ Créer un compte"):
    st.switch_page("pages/joueur_creation_page.py")
if st.button("Réinitialiser la base de données"):
    try:
        r = requests.get(f"{API_URL}/reset_database")
        if r.status_code == 200:
            st.success("Base de données réinitialisée ✅")
        else:
            st.error(f"Erreur ({r.status_code}) lors de la réinitialisation")
    except requests.RequestException as e:
        st.error(f"Impossible de contacter le serveur API : {e}")
