import time

import streamlit as st

from utils.api_client import api_client

st.title("Play a Coin flip")

joueur = st.session_state.get("joueur")

if not st.session_state.get("joueur"):
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

    st.write(f"Result : **{data['resultat']}**")

    if data["gagnant"] == joueur["pseudo"]:
        st.success("🎉 **You win!**")
        st.balloons()
    else:
        st.warning("😢 **You lose**")


if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")
