# frontend/pages/joueur_creation.py
import streamlit as st

from utils.api_client import api_client

st.title("➕ Création d'un joueur")

if st.button("⬅️ Retour au menu"):
    st.switch_page("pages/main_page.py")

pseudo = st.text_input("Pseudo")
mdp = st.text_input("Mot de passe", type="password")
age = st.number_input("Âge", min_value=1, max_value=120)
mail = st.text_input("Email")
fan_pokemon = st.checkbox("Fan de Pokémon ?")

if st.button("Créer le joueur"):
    joueur = {
        "pseudo": pseudo,
        "mdp": mdp,
        "age": age,
        "mail": mail,
        "fan_pokemon": fan_pokemon,
    }

    response = api_client.post("/joueur/", json=joueur)

    if response:
        if response["status_code"] == 200:
            st.success(f"Joueur {pseudo} créé avec succès ! 🎉")
        else:
            st.error(f"Erreur : {response['data']}")
