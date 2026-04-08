# frontend/pages/player_creation.py
import logging

import streamlit as st

from utils.api_client import api_client

st.title("Create a player account")

username = st.text_input("Username", max_chars=20)
password = st.text_input("Password", type="password")
elo = st.number_input("Elo", min_value=1000, max_value=3000)
email = st.text_input("Email")
pokemon_fan = st.checkbox("Pokemons fan?")

with st.container(horizontal_alignment="center"):
    if st.button("Create", width=150, disabled=not username):
        logging.info("Create player")
        player = {
            "username": username,
            "password": password,
            "elo": elo,
            "email": email,
            "pokemon_fan": pokemon_fan,
        }

        response = api_client.post("/player/", json=player)

        if response:
            if response["status_code"] == 200:
                st.success(f"Player {username} successfully created! 🎉")
                logging.info("Player created successfully")
            else:
                st.error(f"Error: {response['data']}")
                logging.info("Error while creating player")

if st.button("Back to homepage", type="primary"):
    logging.info("Back to homepage")
    st.switch_page("pages/home.py")
