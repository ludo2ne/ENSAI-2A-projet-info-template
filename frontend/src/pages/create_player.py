# frontend/pages/joueur_creation.py
import logging

import streamlit as st

from utils.api_client import api_client

st.title("Create a player account")

pseudo = st.text_input("Username", max_chars=20)
mdp = st.text_input("Password", type="password")
elo = st.number_input("Elo", min_value=1000, max_value=3000)
mail = st.text_input("Email")
fan_pokemon = st.checkbox("Pokemons fan?")

with st.container(horizontal_alignment="center"):
    if st.button("Create", width=150, disabled=not pseudo):
        logging.info("Create player")
        joueur = {
            "pseudo": pseudo,
            "mdp": mdp,
            "elo": elo,
            "mail": mail,
            "fan_pokemon": fan_pokemon,
        }

        response = api_client.post("/joueur/", json=joueur)

        if response:
            if response["status_code"] == 200:
                st.success(f"Player {pseudo} successfully created! 🎉")
                logging.info("Player created successfully")
            else:
                st.error(f"Error: {response['data']}")
                logging.info("Error while creating player")

if st.button("Back to homepage", type="primary"):
    logging.info("Back to homepage")
    st.switch_page("pages/home.py")
