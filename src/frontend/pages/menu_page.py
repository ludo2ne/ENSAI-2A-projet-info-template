import streamlit as st


def menu_page():
    joueur = st.session_state.joueur
    st.title(f"🎮 Menu principal — Bonjour {joueur['pseudo']} !")

    st.write("Choisissez une action :")

    if st.button("📋 Lister les joueurs"):
        st.session_state.go_to("liste_joueurs")

    if st.button("➕ Créer un joueur"):
        st.session_state.go_to("creation_joueur")

    if st.button("🚪 Se déconnecter"):
        st.session_state.joueur = None
        st.session_state.go_to("connexion")
