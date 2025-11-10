# frontend/app.py
import streamlit as st

st.set_page_config(page_title="Gestion des joueurs")
st.title("Interface Joueurs")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Connexion", "Liste des joueurs"])

if page == "Connexion":
    # import local module to keep code organized
    from pages.connexion_page import connexion_page

    connexion_page()
elif page == "Liste des joueurs":
    from pages.joueurs import joueurs_page

    joueurs_page()
