import logging
import time

import streamlit as st

from utils.api_client import api_client

st.title("Play a Coin flip")

joueur = st.session_state.get("joueur")

if not st.session_state.get("joueur"):
    logging.info("Not logged in, return to the home page")
    st.error("Access restricted to logged-in users.")
    time.sleep(1)
    st.switch_page("pages/home.py")

response = api_client.get("/joueur/")

if response["status_code"] != 200:
    st.error("Error loading players")
    st.stop()

joueurs = response["data"]
adversaires = [
    j for j in joueurs if j["id_joueur"] != joueur["id_joueur"] and j["pseudo"] != "admin"
]

if not adversaires:
    st.warning("No opponents available")
    st.stop()

adversaire = st.selectbox("Choose an opponent", adversaires, format_func=lambda j: j["pseudo"])

genre = st.radio("Heads or Tails", ["heads", "tails"])

if st.button("Play"):
    logging.info("Play a game")
    with st.spinner("Wait for it..."):
        time.sleep(1)

    response = api_client.post(
        "/game/",
        json={
            "joueur1_id": joueur["id_joueur"],
            "joueur2_id": adversaire["id_joueur"],
            "choice": genre,
        },
    )

    if response["status_code"] != 200:
        st.error(response["data"])
        st.stop()

    data = response["data"]

    st.write(f"Result : **{data['result']}**")

    if data["winner"] == joueur["pseudo"]:
        st.success(f"""🎉 **You win!**\n\nYour new Elo rating is {data["new_elo1"]}""")
        st.balloons()
    else:
        st.warning(f"""😢 **You lose**\n\nYour new Elo rating is {data["new_elo1"]}""")

    logging.info("Game is over")


if st.button("Back to menu", type="primary"):
    logging.info("Back to player menu")
    st.switch_page("pages/player_menu.py")
