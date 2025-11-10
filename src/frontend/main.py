# frontend/app.py
import streamlit as st
from pages.connexion_page import connexion_page
from pages.joueur.joueur_creation_page import joueur_creation_page
from pages.joueur.joueurs_liste_page import joueurs_liste_page
from pages.menu_page import menu_page

st.set_page_config(page_title="Gestion des joueurs", page_icon="🎮", layout="centered")

hide_pages_style = """
    <style>
        /* cache la liste des pages à gauche */
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_pages_style, unsafe_allow_html=True)

session_defaults = {
    "joueur": None,
    "page": "connexion",
}
for key, value in session_defaults.items():
    st.session_state.setdefault(key, value)

PAGES = {
    "connexion": connexion_page,
    "menu": menu_page,
    "liste_joueurs": joueurs_liste_page,
    "creation_joueur": joueur_creation_page,
}


def go_to(page: str):
    """Change la page active et rafraîchit l'affichage."""
    st.session_state.page = page
    st.rerun()


st.session_state.go_to = go_to

if st.session_state.joueur is None and st.session_state.page != "connexion":
    go_to("connexion")

page_func = PAGES.get(st.session_state.page, menu_page)
page_func()
