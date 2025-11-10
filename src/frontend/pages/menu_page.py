import time

import streamlit as st

joueur = st.session_state.get("joueur")

st.title("🎮 Menu principal")

if joueur is None:
    st.error("Accès non autorisé. Veuillez vous connecter.")
    time.sleep(1)
    st.switch_page("main_page.py")

st.badge(f"Bonjour {joueur['pseudo']} !", color="orange")

st.write("Choisissez une action :")

if st.button("📋 Lister les joueurs"):
    st.switch_page("pages/joueur_liste_page.py")
if st.button("➕ Créer un joueur"):
    st.switch_page("pages/joueur_creation_page.py")
if st.button("🚪 Se déconnecter"):
    st.session_state.joueur = None
    st.switch_page("main_page.py")
