import logging

import streamlit as st
from streamlit import config

from utils.api_client import api_client

if "joueur" in st.session_state:
    st.switch_page("pages/player_menu.py")

st.set_page_config(page_title="Coin flip game", page_icon="🪙", layout="centered")

st.markdown(
    f"""
    <div style="text-align:center">
        <h1 style="color:{config.get_option("theme.primaryColor")}">Coin flip game</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

pseudo = st.text_input("Pseudo", placeholder="Enter username")
mdp = st.text_input("Password", type="password", placeholder="Enter password")

with st.container(horizontal_alignment="center"):
    if st.button("Log in"):
        logging.info(f"{pseudo} is trying to log in")
        response = api_client.post("/connexion", json={"pseudo": pseudo, "mdp": mdp})

        if response:
            if response["status_code"] == 200:
                logging.info(f"{pseudo} successfully logged in")
                joueur = response["data"]
                st.session_state["joueur"] = joueur
                st.success(f"Welcome {joueur['pseudo']} ! 🎉")
                st.switch_page("pages/player_menu.py")
            elif response["status_code"] == 401:
                logging.info("Connection error")
                st.error("Invalid credentials")
            else:
                logging.info("Connection error")
                st.error(f"Server error: {response['data']}")

st.space("small")

if st.button("Sign Up"):
    logging.info("Create an account")
    st.switch_page("pages/create_player.py")

if st.button("Reset Database", type="primary"):
    logging.info("Reset the database")
    response = api_client.get("/reset_database")

    if response:
        logging.info("Database successfully reset")
        st.toast("Database successfully reset ✅")
    else:
        logging.info("Error during database reset")
        st.toast("Error during database reset ❌")
