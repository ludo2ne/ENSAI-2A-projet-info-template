import logging
import time

import streamlit as st

from utils.api_client import api_client

st.title("Play a Coin flip")

player = st.session_state.get("player")

if not st.session_state.get("player"):
    logging.info("Not logged in, return to the home page")
    st.error("Access restricted to logged-in users.")
    time.sleep(1)
    st.switch_page("pages/home.py")

response = api_client.get("/player/")

if response["status_code"] != 200:
    st.error("Error loading players")
    st.stop()

players = response["data"]
adversaires = [
    j for j in players if j["id_player"] != player["id_player"] and j["username"] != "admin"
]

if not adversaires:
    st.warning("No opponents available")
    st.stop()

adversaire = st.selectbox("Choose an opponent", adversaires, format_func=lambda j: j["username"])

genre = st.radio("Heads or Tails", ["heads", "tails"])

if st.button("Play"):
    logging.info("Play a game")
    with st.spinner("Wait for it..."):
        time.sleep(1)

    response = api_client.post(
        "/game/",
        json={
            "player1_id": player["id_player"],
            "player2_id": adversaire["id_player"],
            "choice": genre,
        },
    )

    if response["status_code"] != 200:
        st.error(response["data"])
        st.stop()

    data = response["data"]

    st.write(f"Result : **{data['result']}**")

    if data["winner"] == player["username"]:
        st.success(f"""🎉 **You win!**\n\nYour new Elo rating is {data["new_elo1"]}""")
        st.balloons()
    else:
        st.warning(f"""😢 **You lose**\n\nYour new Elo rating is {data["new_elo1"]}""")

    logging.info("Game is over")


if st.button("Back to menu", type="primary"):
    logging.info("Back to player menu")
    st.switch_page("pages/player_menu.py")
